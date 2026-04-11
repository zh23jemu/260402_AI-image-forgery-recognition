# -*- coding: utf-8 -*-
""" A simple test script. 
"""

import os
import torch
from tqdm import tqdm
from torch.amp import autocast
import timm
from einops import rearrange
from torchmetrics.classification import Accuracy, AveragePrecision

from model.prototypical_utils import compute_prototypical_loss
from datasets import setup_val_dataloader
from util.parser import TestParser
from util.utils import load_model
import util.logger as logger


def resolve_data_root(data_root):
    if os.path.isabs(data_root) and os.path.exists(data_root):
        return data_root

    candidates = [
        os.path.abspath(data_root),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", data_root)),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "GenImage")),
    ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return os.path.abspath(data_root)


# no ddp setting
def main(): 
    #################### prepare device ####################
    args = TestParser().args
    args.data_root = resolve_data_root(args.data_root)
    args.device = torch.device("cuda")
    # terminal writer and file writer
    logger.setup(log_dir=args.output_dir, device=None)
    ############################################################


    #################### setup dataset and dataloader ####################
    logger.info("Creating test data loader...")
    logger.info(f"Resolved data root: {args.data_root}")

    # data we use in GenImage
    if args.test_class.upper() == "NONE": # test on all classes
        TEST_FOLDERS = ["real", "Midjourney", "SD", "ADM", "GLIDE", "VQDM", "BigGAN"]
    else: # test on single class
        TEST_FOLDERS = ["real", args.test_class]
    
    test_dataloaders = {
        folder: setup_val_dataloader(
            folder_path=os.path.join(args.data_root, folder, "val"), 
            batch_size=args.num_support_test + args.num_query_test, 
            num_workers=args.num_workers, 
        ) for folder in TEST_FOLDERS
    }
    ############################################################

    
    #################### setup model ####################
    logger.info("Creating model 'resnet50'... ")
    # For evaluation we load the full detector weights from CKPT_PATH, so we
    # avoid fetching ImageNet pretrained weights from the internet.
    model = timm.create_model("resnet50", pretrained=False, num_classes=1024)
    logger.info(f"Loading checkpoint from {args.ckpt_path} ...")
    load_model(args.ckpt_path, model=model)
    logger.info("Checkpoint loaded. Moving model to CUDA ...")

    # deployment
    model = model.to(args.device)
    logger.info("Model moved to CUDA successfully. ")
    ############################################################
    

    #################### testing ####################
    logger.info(f"Start testing with checkpoint {args.ckpt_path}. ")
    model.eval()

    acc_calculator = Accuracy(task="multiclass", num_classes=2)
    ap_calculator = AveragePrecision(task="multiclass", num_classes=2, thresholds=10)

    with torch.no_grad(): 
        for i in range(1, len(TEST_FOLDERS)): 
            prob_list = []
            label_list = []
            for (neg_batch, _), (pos_batch, _) in tqdm(zip(test_dataloaders["real"], test_dataloaders[TEST_FOLDERS[i]])): 
                batch_data = torch.stack([neg_batch, pos_batch], dim=0) # (2, task_size, c, h, w)
                batch_data = batch_data.to(args.device)

                batch_data = rearrange(batch_data, 'n b c h w -> (n b) c h w')
                labels = torch.arange(0, args.num_class_test, device=args.device).repeat(args.num_query_test)

                with autocast(enabled=args.use_fp16, device_type="cuda"):
                    outputs = model(batch_data)
                outputs = rearrange(outputs, '(n b) l -> 1 b n l', n=args.num_class_test) # we change the subscript sequence

                _, scores = compute_prototypical_loss(outputs, labels, args.num_support_test)

                prob = scores.softmax(dim=-1).cpu()
                labels = labels.cpu()

                prob_list.append(prob)
                label_list.append(labels)
            
            total_prob = torch.cat(prob_list, dim=0)
            total_label = torch.cat(label_list, dim=0)
            acc = acc_calculator(total_prob, total_label)
            ap = ap_calculator(total_prob, total_label)

            logger.info(f'Evaluation on {TEST_FOLDERS[i]} done. evaluating num: {len(total_prob)}, accuracy: {acc}, average precision: {ap}. ')
    ############################################################


if __name__ == '__main__': 
    main()

