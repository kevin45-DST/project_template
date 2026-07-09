from pathlib import Path

from loaders.metrics_loader import MetricsLoader

from views.metrics_view import MetricsView


class Dashboard:

    def __init__(
        self,
        report_path: Path,
    ) -> None:

        self.report_path = report_path

    def run(self) -> None:

        metrics = MetricsLoader(
            self.report_path
        ).load()

        MetricsView(
            metrics,
            self.report_path,
        ).show()