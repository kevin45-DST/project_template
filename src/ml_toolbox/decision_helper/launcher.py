from pathlib import Path
import os
import subprocess
import sys


class Launcher:

    def __init__(
        self,
        report_path: Path,
    ) -> None:

        self.report_path = report_path

    def run(self) -> None:

        os.environ["DECISION_HELPER_REPORT_PATH"] = str(
            self.report_path
        )

        app = (
            Path(__file__).parent
            / "app.py"
        )

        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(app),
            ]
        )