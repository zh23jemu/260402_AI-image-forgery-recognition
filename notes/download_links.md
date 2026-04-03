# 下载入口整理

## 1. FSD

- 官方仓库：<https://github.com/teheperinko541/Few-Shot-AIGI-Detector>
- 论文：<https://arxiv.org/abs/2501.08763>
- GenImage 下载参考仓库：<https://github.com/GenImage-Dataset/GenImage>
- 百度网盘数据入口：提取码 `ztf1`
- FSD checkpoint：官方 README 中给出的百度网盘入口，提取码 `icml`

## 2. Stay-Positive

- 官方仓库：<https://github.com/AniSundar18/AlignedForensics>
- 项目页：<https://anisundar18.github.io/Stay-Positive/>
- 论文：<https://openreview.net/forum?id=VNLmfMJi3w>
- 预训练模型：
  - `Corvi +`
  - `Rajan/Ours +`
- 评估数据入口：官方 README 中提供 Hugging Face 链接

## 3. GenImage

- 官方仓库：<https://github.com/GenImage-Dataset/GenImage>
- Google Drive：<https://drive.google.com/drive/folders/1jGt10bwTbhEZuGXLyvrCuxOI0cBqQ1FS?usp=sharing>
- 百度网盘信息见官方 README

## 4. 当前阶段建议优先下载

如果只围绕论文初稿和最小代码准备推进，当前推荐优先准备：

1. FSD 官方代码
2. Stay-Positive 官方代码
3. FSD checkpoint
4. Stay-Positive 预训练模型
5. GenImage 的 `Stable Diffusion V1.4`

## 5. 当前网络状态说明

本地已尝试通过 `git clone --depth 1` 在线克隆 FSD 和 Stay-Positive 官方仓库，但当前网络环境返回连接被重置。因此目前采用的策略是：

- 先把本地目录和文档骨架搭好
- 由用户手动下载 ZIP 或在网络稳定时重新克隆
- 下载完成后再将代码放入对应目录
