# build.py — entry point of a maintained presentation source.
# Each slide lives in slides/slideNN.py exposing build(prs) — or, for small decks
# (<= 8 slides), slide functions may live directly in this file.
# Regenerating the deck = `python build.py` (deterministic, idempotent).

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pptx import Presentation
import theme as T

def new_presentation():
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H
    return prs

def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # fully blank layout

def main():
    prs = new_presentation()

    import importlib
    slides_dir = pathlib.Path(__file__).parent / "slides"
    if slides_dir.exists():
        for mod_path in sorted(slides_dir.glob("slide*.py")):
            mod = importlib.import_module(f"slides.{mod_path.stem}")
            mod.build(prs, blank_slide(prs))

    out = pathlib.Path(__file__).parent.parent / "presentation.pptx"
    prs.save(out)
    print(f"saved: {out}")

if __name__ == "__main__":
    main()
