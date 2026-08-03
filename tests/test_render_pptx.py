from __future__ import annotations

import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[1]
RENDER_SCRIPT = REPO_DIR / "skill" / "make-ppt" / "scripts" / "render_pptx.sh"


def write_executable(path: Path, source: str) -> None:
    path.write_text(source, encoding="utf-8", newline="\n")
    path.chmod(0o755)


def bash_path(path: Path) -> str:
    if os.name != "nt":
        return str(path)
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    suffix = "/".join(resolved.parts[1:]).replace("\\", "/")
    kernel = subprocess.run(
        ["bash", "-lc", "uname -s"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    prefix = f"/mnt/{drive}" if kernel == "Linux" else f"/{drive}"
    return f"{prefix}/{suffix}"


def run_render(
    mock_bin: Path, deck: Path, output: Path, trace: Path
) -> subprocess.CompletedProcess[str]:
    command = (
        f"PATH={shlex.quote(bash_path(mock_bin))}:/usr/bin:/bin "
        f"TRACE_FILE={shlex.quote(bash_path(trace))} "
        f"bash {shlex.quote(bash_path(RENDER_SCRIPT))} "
        f"{shlex.quote(bash_path(deck))} {shlex.quote(bash_path(output))}"
    )
    return subprocess.run(
        ["bash", "-c", command],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )


class RenderPptxTests(unittest.TestCase):
    def test_macos_powerpoint_is_used_without_libreoffice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            mock_bin = root / "bin"
            mock_bin.mkdir()
            deck = root / "deck.pptx"
            deck.write_bytes(b"fake pptx")
            output = root / "preview"
            trace = root / "osascript.trace"

            write_executable(mock_bin / "uname", "#!/usr/bin/env bash\nprintf 'Darwin\\n'\n")
            write_executable(
                mock_bin / "open",
                "#!/usr/bin/env bash\n"
                "[ \"${1:-}\" = '-Ra' ] && "
                "[ \"${2:-}\" = 'Microsoft PowerPoint' ]\n",
            )
            write_executable(
                mock_bin / "osascript",
                "#!/usr/bin/env bash\n"
                "printf '%s\\n' \"$@\" > \"$TRACE_FILE\"\n"
                "printf 'fake pdf' > \"$3\"\n",
            )
            write_executable(
                mock_bin / "pdftoppm",
                "#!/usr/bin/env bash\n"
                "for arg in \"$@\"; do prefix=\"$arg\"; done\n"
                "printf 'png' > \"${prefix}-1.png\"\n"
                "printf 'png' > \"${prefix}-2.png\"\n",
            )

            result = run_render(mock_bin, deck, output, trace)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(trace.exists(), "macOS PowerPoint adapter was not invoked")
            self.assertTrue((output / "slide-01.png").exists())
            self.assertTrue((output / "slide-02.png").exists())

    def test_macos_powerpoint_failure_falls_back_to_libreoffice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            mock_bin = root / "bin"
            mock_bin.mkdir()
            deck = root / "deck.pptx"
            deck.write_bytes(b"fake pptx")
            output = root / "preview"
            trace = root / "osascript.trace"

            write_executable(mock_bin / "uname", "#!/usr/bin/env bash\nprintf 'Darwin\\n'\n")
            write_executable(mock_bin / "open", "#!/usr/bin/env bash\nexit 0\n")
            write_executable(
                mock_bin / "osascript",
                "#!/usr/bin/env bash\n"
                "printf '%s\\n' \"$@\" > \"$TRACE_FILE\"\n"
                "exit 3\n",
            )
            write_executable(
                mock_bin / "soffice",
                "#!/usr/bin/env bash\n"
                "while [ \"$#\" -gt 0 ]; do\n"
                "  if [ \"$1\" = '--outdir' ]; then shift; out=\"$1\"; fi\n"
                "  case \"$1\" in *.pptx) deck=\"$1\" ;; esac\n"
                "  shift\n"
                "done\n"
                "name=\"$(basename \"${deck%.pptx}\")\"\n"
                "printf 'fake pdf' > \"$out/$name.pdf\"\n",
            )
            write_executable(
                mock_bin / "pdftoppm",
                "#!/usr/bin/env bash\n"
                "for arg in \"$@\"; do prefix=\"$arg\"; done\n"
                "printf 'png' > \"${prefix}-1.png\"\n",
            )

            result = run_render(mock_bin, deck, output, trace)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("falling back to LibreOffice", result.stderr)
            self.assertTrue(trace.exists())
            self.assertTrue((output / "slide-01.png").exists())


if __name__ == "__main__":
    unittest.main()
