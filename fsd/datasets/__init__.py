import warnings

from PIL import UnidentifiedImageError
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, DistributedSampler
from torchvision import transforms
import torch.distributed as dist


class SafeImageFolder(ImageFolder):
    def __getitem__(self, index):
        path, target = self.samples[index]
        try:
            sample = self.loader(path)
        except (UnidentifiedImageError, OSError) as exc:
            warnings.warn(f"Skip unreadable image: {path} ({exc})")
            return self.__getitem__((index + 1) % len(self.samples))

        if self.transform is not None:
            sample = self.transform(sample)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return sample, target

def setup_infinity_train_dataloader(
    folder_path, 
    batch_size=20, 
    num_workers=16, 
    pin_memory=True, 
    drop_last=True
):
    transform = transforms.Compose([
        transforms.Resize(256), 
        transforms.RandomCrop(224), 
        transforms.RandomHorizontalFlip(), 
        transforms.ToTensor(),
    ])
    dataset = SafeImageFolder(folder_path, transform=transform) # As GenImage dataset is very large, so it's ok for different size of each class
    sampler = DistributedSampler(dataset) if dist.is_initialized() else None

    loader = DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=(sampler is None), 
        sampler=sampler, 
        num_workers=num_workers, 
        pin_memory=pin_memory, 
        drop_last=drop_last
    )
    
    # adding epoch control
    epoch = 0

    while True: 
        if sampler is not None: 
            sampler.set_epoch(epoch)
        epoch += 1
        yield from loader


def setup_val_dataloader(
    folder_path, 
    batch_size=20, 
    num_workers=16, 
    pin_memory=True, 
    drop_last=True
): 
    transform = transforms.Compose([ 
        transforms.CenterCrop(224), 
        transforms.ToTensor(), 
    ])

    return DataLoader(
        SafeImageFolder(folder_path, transform=transform), 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=num_workers, 
        pin_memory=pin_memory, 
        drop_last=drop_last, 
    )
