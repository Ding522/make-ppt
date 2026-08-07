from __future__ import annotations

import unittest
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_DIR / "skill" / "make-ppt"


class SkillPolicyTests(unittest.TestCase):
    def test_takeaway_is_default_off_without_reserved_space(self) -> None:
        planner = (SKILL_DIR / "references" / "ppt-planner-role.md").read_text(
            encoding="utf-8"
        )
        style = (SKILL_DIR / "references" / "style-guide.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Takeaway is default-off", planner)
        self.assertIn("Do not reserve takeaway space", style)

    def test_native_table_policy_requires_structured_schema_and_object_qa(self) -> None:
        outline = (SKILL_DIR / "templates" / "outline-template.md").read_text(
            encoding="utf-8"
        )
        rules = (SKILL_DIR / "references" / "pptx-generation-rules.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("### Table Schema", outline)
        self.assertIn("add_native_table", rules)
        self.assertIn("validate_pptx_structure.py", rules)

    def test_narrative_review_is_planned_without_per_slide_bridge_fields(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        planner = (SKILL_DIR / "references" / "ppt-planner-role.md").read_text(
            encoding="utf-8"
        )
        builder = (SKILL_DIR / "references" / "ppt-builder-role.md").read_text(
            encoding="utf-8"
        )
        outline = (SKILL_DIR / "templates" / "outline-template.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Narrative Review", skill)
        self.assertIn("section-continuity pass", planner)
        self.assertIn("Slides NN -> NN", outline)
        self.assertIn("previous/current/next field", planner)
        self.assertIn("Preserve the approved slide order", builder)
        self.assertNotIn("### Section Continuity", outline)

    def test_font_pair_is_pinned_to_noto_sans_tc_and_consolas(self) -> None:
        theme = (SKILL_DIR / "assets" / "src-template" / "theme.py").read_text(
            encoding="utf-8"
        )
        style = (SKILL_DIR / "references" / "style-guide.md").read_text(
            encoding="utf-8"
        )
        rules = (SKILL_DIR / "references" / "pptx-generation-rules.md").read_text(
            encoding="utf-8"
        )

        self.assertIn('FONT_CJK = "Noto Sans TC"', theme)
        self.assertIn('FONT_MONO = "Consolas"', theme)
        self.assertNotIn("Microsoft JhengHei", theme)
        self.assertNotIn("JetBrains Mono", theme)
        self.assertIn("**Noto Sans TC**", style)
        self.assertIn("**Consolas**", style)
        self.assertIn("`Noto Sans TC`", rules)
        self.assertIn("`Consolas`", rules)


if __name__ == "__main__":
    unittest.main()
