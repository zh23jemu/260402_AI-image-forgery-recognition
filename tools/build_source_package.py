from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(r"C:\Coding\260402_AI-image-forgery-recognition")
OUT_DIR = ROOT / "deliverables"
ZIP_PATH = OUT_DIR / "AI伪造图像识别_程序源码包.zip"


INCLUDE_DIRS = [
    "fsd",
    "stay_positive",
    "tools",
]

INCLUDE_FILES = [
    "README.md",
    "docs/项目交付总说明_合并版.md",
]

EXCLUDE_DIR_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    "output",
    "logs",
    "data",
    "analysis",
    "deliverables",
}

EXCLUDE_SUFFIXES = {
    ".pth",
    ".pt",
    ".ckpt",
    ".tar",
    ".gz",
    ".zip",
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".slurm",
}


def should_skip(path: Path) -> bool:
    if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
        return True
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    return False


def iter_files() -> list[Path]:
    files: list[Path] = []
    for rel in INCLUDE_FILES:
        path = ROOT / rel
        if path.exists() and path.is_file():
            files.append(path)
    for rel in INCLUDE_DIRS:
        base = ROOT / rel
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if should_skip(path.relative_to(ROOT)):
                continue
            files.append(path)
    # 去重并保持稳定顺序
    unique = sorted({p.relative_to(ROOT).as_posix(): p for p in files}.values(), key=lambda x: x.relative_to(ROOT).as_posix())
    return unique


def build_zip() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = iter_files()
    with ZipFile(ZIP_PATH, "w", compression=ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, arcname=path.relative_to(ROOT).as_posix())
    return ZIP_PATH


def main() -> None:
    zip_path = build_zip()
    print(f"zip_saved={zip_path}")


if __name__ == "__main__":
    main()
