# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class runId:

    @staticmethod
    def create() -> str:
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S%f"
        )

        return f"run_{timestamp}"