from __future__ import annotations

import unittest
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_DIR / "skill" / "make-ppt"


class SkillPolicyTests(unittest.TestCase):
    def test_cost_modes_are_explicit_and_direction_clarity_does_not_imply_strict(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        policy = (
            SKILL_DIR / "references" / "cost-control-workflow.md"
        ).read_text(encoding="utf-8")
        outline = (SKILL_DIR / "templates" / "outline-template.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("`standard` is the default", policy)
        self.assertIn("A clear prompt never activates `strict`", policy)
        self.assertIn("at least two of these three fields", policy)
        self.assertIn("`explore` and `strict` require explicit user intent", skill)
        self.assertIn("- Cost Mode:", outline)
        self.assertIn("- Direction Lock:", outline)

    def test_narrative_fork_is_compact_conditional_and_hard_paused(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        policy = (
            SKILL_DIR / "references" / "cost-control-workflow.md"
        ).read_text(encoding="utf-8")
        template = (
            SKILL_DIR / "templates" / "narrative-forks-template.md"
        ).read_text(encoding="utf-8")

        self.assertIn("conditional hard pause", skill)
        self.assertIn("exactly three compact narrative", policy)
        self.assertIn("Do not write three outlines", policy)
        self.assertIn("## Axis A", template)
        self.assertIn("## Axis B", template)
        self.assertIn("## Axis C", template)
        self.assertIn("Stop and wait", template)

    def test_outline_approval_is_mandatory_and_invalidated_by_structural_changes(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        policy = (
            SKILL_DIR / "references" / "cost-control-workflow.md"
        ).read_text(encoding="utf-8")

        self.assertIn("This checkpoint is mandatory in every mode", skill)
        self.assertIn("No mode may skip this checkpoint", policy)
        self.assertIn("slides are added or removed", policy)
        self.assertIn("do not invalidate approval", policy)

    def test_non_small_edits_get_impact_record_and_rebuild_confirmation(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        policy = (
            SKILL_DIR / "references" / "cost-control-workflow.md"
        ).read_text(encoding="utf-8")
        localized = (
            SKILL_DIR / "references" / "localized-edit-principle.md"
        ).read_text(encoding="utf-8")
        template = (
            SKILL_DIR / "templates" / "edit-impact-template.md"
        ).read_text(encoding="utf-8")
        readme = (REPO_DIR / "README.md").read_text(encoding="utf-8")

        for classification in (
            "small-localized",
            "single-slide-structural",
            "cross-slide",
            "narrative-restructure",
            "full-rebuild-candidate",
        ):
            self.assertIn(classification, policy)

        self.assertIn("affected slides exceed 30%", policy)
        self.assertIn("shared theme tokens or shared primitives", policy)
        self.assertIn("`確認 full rebuild`", policy)
        self.assertIn("an additional flag, not a replacement", policy)
        self.assertIn("enforce both\ngates", policy)
        self.assertIn("re-present the outline checkpoint", localized)
        self.assertNotIn("affected slides exceed 30%", skill)
        self.assertNotIn("30% of slides", localized)
        self.assertIn("- Why Localized Edit Is Insufficient:", template)
        self.assertIn("- Recommended Rollback Stage:", template)
        self.assertIn("- Cost / Risk Note:", template)
        self.assertIn("append + full-rebuild-candidate", template)
        self.assertIn("slide\nadditions/removals invalidate", readme)
        self.assertNotIn("slide-count changes", readme)

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

    def test_visible_copy_uses_taiwan_traditional_chinese(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        planner = (SKILL_DIR / "references" / "ppt-planner-role.md").read_text(
            encoding="utf-8"
        )
        builder = (SKILL_DIR / "references" / "ppt-builder-role.md").read_text(
            encoding="utf-8"
        )
        guide = (SKILL_DIR / "references" / "taiwan-language-guide.md").read_text(
            encoding="utf-8"
        )
        outline = (SKILL_DIR / "templates" / "outline-template.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Taiwan Traditional Chinese (`zh-TW`)", skill)
        self.assertIn("`references/taiwan-language-guide.md`", planner)
        self.assertIn("`references/taiwan-language-guide.md`", builder)
        self.assertIn("按兩下", guide)
        self.assertIn("Software options → `設定`", guide)
        self.assertIn("official product/UI labels", guide)
        self.assertIn("verbatim source quotations", guide)
        self.assertIn("台灣繁體中文（zh-TW", outline)
        self.assertIn("scripts/lint_zh_tw.py", skill)
        self.assertIn("checker never rewrites content", guide)


if __name__ == "__main__":
    unittest.main()
