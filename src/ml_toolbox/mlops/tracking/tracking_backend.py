# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from abc import ABC, abstractmethod
from typing import Any


class TrackingBackend(ABC):
    """
    Interface définissant les opérations de tracking.

    Cette classe représente le contrat que doit respecter
    toute implémentation de tracking.

    Le framework ne dépend pas d'une solution particulière
    (MLflow, Weights & Biases, Azure ML...).

    Chaque backend doit gérer :
    - La création d'une experience
    - l'ouverture d'une expérience 
    - l'enregistrement des paramètres 
    - l'enregistrement des métriques 
    - l'enregistrement des artefacts
    """
       
    @abstractmethod
    def initialize_experiment(
        self
    ) -> None:
        """
        Crée une expérience de tracking.
        """
        pass
    
    @abstractmethod
    def start_run(
        self,
        run_name: str,
    ) -> None:
        """
        Démarre une expérience de tracking.
        """
        pass

    @abstractmethod
    def log_params(
        self,
        params: dict[str, Any],
    ) -> None:
        """
        Enregistre les paramètres d'une expérience.
        """
        pass

    @abstractmethod
    def log_metrics(
        self,
        metrics: dict[str, float],
    ) -> None:
        """
        Enregistre les métriques d'une expérience.
        """
        pass

    @abstractmethod
    def log_artifact(
        self,
        path: str,
    ) -> None:
        """
        Enregistre un artefact associé à une expérience.
        """
        pass

    @abstractmethod
    def end_run(self) -> None:
        """
        Termine une expérience de tracking.
        """
        pass