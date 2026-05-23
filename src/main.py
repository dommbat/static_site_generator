import os
import shutil
from pathlib import Path


def copy_dir_clean(src, dst):
    src_path = Path(src).resolve()
    dst_path = Path(dst).resolve()

    if not src_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {src_path}")

    if dst_path.exists():
        for child in dst_path.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        dst_path.mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(src_path):
        root_path = Path(root)
        rel_root = root_path.relative_to(src_path)
        target_root = dst_path.joinpath(rel_root)
        target_root.mkdir(parents=True, exist_ok=True)

        for name in files:
            src_file = root_path / name
            dst_file = target_root / name
            shutil.copy2(src_file, dst_file)
            print(f"Copied {src_file} -> {dst_file}")

    print(f"Finished copying from {src_path} to {dst_path}")


def main():
    repo_root = Path(__file__).resolve().parent.parent
    source = repo_root / "static"
    destination = repo_root / "public"
    copy_dir_clean(source, destination)


if __name__ == "__main__":
    main()
