#!/usr/bin/env python3
"""create_contact_sheet.py <preview_dir> <output.png> [--cols N]
Combine slide-NN.png previews into a labeled contact sheet."""
import sys, glob, os, math, re
from PIL import Image, ImageDraw

def slide_number(path):
    match = re.fullmatch(r"slide-(\d+)\.png", os.path.basename(path), re.IGNORECASE)
    if not match:
        raise ValueError(f"invalid preview filename: {path}")
    return int(match.group(1))

def main():
    prev, out = sys.argv[1], sys.argv[2]
    cols = int(sys.argv[sys.argv.index("--cols")+1]) if "--cols" in sys.argv else 4
    files = sorted(glob.glob(os.path.join(prev, "slide-*.png")), key=slide_number)
    if not files:
        sys.exit("no slide-*.png in " + prev)
    thumb_w = 480
    ims = []
    for f in files:
        im = Image.open(f).convert("RGB")
        im = im.resize((thumb_w, int(im.size[1]*thumb_w/im.size[0])))
        ims.append(im)
    th = ims[0].size[1]; pad, label_h = 12, 22
    rows = math.ceil(len(ims)/cols)
    sheet = Image.new("RGB", (cols*(thumb_w+pad)+pad, rows*(th+label_h+pad)+pad), "#FAF8F4")
    d = ImageDraw.Draw(sheet)
    for i, (path, im) in enumerate(zip(files, ims)):
        x = pad + (i % cols)*(thumb_w+pad)
        y = pad + (i // cols)*(th+label_h+pad)
        sheet.paste(im, (x, y))
        d.rectangle([x-1, y-1, x+thumb_w, y+th], outline="#DED8CE")
        d.text((x, y+th+4), os.path.splitext(os.path.basename(path))[0], fill="#8A8177")
    sheet.save(out)
    print(out)

if __name__ == "__main__":
    main()
