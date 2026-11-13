#!/usr/bin/env python3
"""news-image-01 entry: copy the pre-rendered front page to the output dir.

Standard library only. The PNG is rendered locally by generate.py and
shipped in the repo; the grading runtime has no Pillow, so this program
just copies entry.png to MAKEFUN_OUTPUT_DIR (default /output).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
