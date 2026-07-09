# Racine projet pour imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.ml_toolbox.decision_helper.launcher import Launcher
from config.config_manager import ConfigManager


class DecisionHelper:

    def __init__(
        self,
    ) -> None:
        config = ConfigManager(
                "config/paths.yaml"
                )
        report_path = config.get(
                "reports.search"
                )
        self.report_path = Path(report_path)

    def run(self) -> None:

        launcher = Launcher(
            self.report_path,
        )

        launcher.run()
        
if __name__ == "__main__":

    helper = DecisionHelper()

    helper.run()