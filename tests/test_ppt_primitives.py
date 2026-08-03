from __future__ import annotations

import importlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches


REPO_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO_DIR / "skill" / "make-ppt" / "assets" / "src-template"
VALIDATOR = (
    REPO_DIR / "skill" / "make-ppt" / "scripts" / "validate_pptx_structure.py"
)

sys.path.insert(0, str(TEMPLATE_DIR))
P = importlib.import_module("primitives")


def new_slide():
    presentation = Presentation()
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    return presentation, slide


class NativeTablePrimitiveTests(unittest.TestCase):
    def test_add_native_table_creates_one_real_table_object(self) -> None:
        _, slide = new_slide()

        frame = P.add_native_table(
            slide,
            Inches(0.6),
            Inches(2.2),
            Inches(12.1),
            Inches(3.8),
            headers=["技法", "落地"],
            rows=[
                ["冪等", "Idempotency-Key + notification_log"],
                ["併發控制", "If-Match / ETag + 樂觀鎖"],
            ],
            col_widths=[0.2, 0.8],
            row_label_col=0,
        )

        self.assertTrue(frame.has_table)
        self.assertEqual(1, sum(shape.has_table for shape in slide.shapes))
        self.assertEqual("技法", frame.table.cell(0, 0).text)
        self.assertEqual("If-Match / ETag + 樂觀鎖", frame.table.cell(2, 1).text)
        self.assertEqual(14, frame.table.cell(1, 1).text_frame.paragraphs[0].runs[0].font.size.pt)

    def test_structure_validator_rejects_fake_table_and_accepts_native_table(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_path = root / "fake.pptx"
            real_path = root / "real.pptx"

            fake_prs, fake_slide = new_slide()
            fake_slide.shapes.add_textbox(
                Inches(0.5), Inches(0.5), Inches(4), Inches(0.5)
            ).text = "技法"
            fake_slide.shapes.add_textbox(
                Inches(4.5), Inches(0.5), Inches(4), Inches(0.5)
            ).text = "落地"
            fake_prs.save(fake_path)

            real_prs, real_slide = new_slide()
            P.add_native_table(
                real_slide,
                Inches(0.5),
                Inches(0.5),
                Inches(8),
                Inches(2),
                headers=["技法", "落地"],
                rows=[["冪等", "Idempotency-Key"]],
            )
            real_prs.save(real_path)

            fake = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
                    str(fake_path),
                    "--require-table-slides",
                    "1",
                ],
                capture_output=True,
                text=True,
            )
            real = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
                    str(real_path),
                    "--require-table-slides",
                    "1",
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(0, fake.returncode)
            self.assertIn("missing a native table object", fake.stderr)
            self.assertEqual(0, real.returncode, real.stderr)


if __name__ == "__main__":
    unittest.main()
