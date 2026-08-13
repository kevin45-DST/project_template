# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from abc import ABC, abstractmethod
from typing import Any


class EvaluationBackend(ABC):
    """
    Interface des backends d'évaluation.
    """

    @abstractmethod
    def evaluate(
        self,
    ) -> dict[str, Any]:
        pass