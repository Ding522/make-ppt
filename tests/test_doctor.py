from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from client_registry import load_registry


REPO_DIR = Path(__file__).resolve().parents[1]
DOCTOR = REPO_DIR / "doctor.py"
INSTALLER = REPO_DIR / "install.py"


class DoctorTests(unittest.TestCase):
    def test_doctor_reports_every_registered_client_from_one_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project_dir = Path(temporary)
            subprocess.run(
                [
                    sys.executable,
                    str(INSTALLER),
                    "--client",
                    "all",
                    "--scope",
                    "project",
                    "--project-dir",
                    str(project_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(DOCTOR),
                    "--client",
                    "all",
                    "--scope",
                    "project",
                    "--project-dir",
                    str(project_dir),
                    "--json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            report = json.loads(result.stdout)
            self.assertEqual(
                set(load_registry(REPO_DIR / "integrations" / "clients.json")),
                set(report["clients"]),
            )
            for client in report["clients"].values():
                self.assertTrue(client["skill"]["installed"])
                self.assertTrue(
                    all(agent["installed"] for agent in client["agents"].values())
                )


if __name__ == "__main__":
    unittest.main()
