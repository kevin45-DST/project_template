import json
from pathlib import Path

import pandas as pd


class MetricsLoader:

    def __init__(
        self,
        report_path: Path,
    ) -> None:

        self.report_path = report_path

    def load(self) -> pd.DataFrame:

        return pd.read_csv(
            self.report_path / "report.csv"
        )
        
    def load_confusion_matrix(
        self,
        run_id: str,
    ) -> dict:

        file_path = (
            self.report_path
            / "confusion_matrix"
            / f"{run_id}_confusion_matrix.json"
        )

        with open(
            file_path,
            encoding="utf-8",
        ) as file:

            return json.load(file)