from pathlib import Path
from typing import Any

from config.config_manager import ConfigManager

from src.utils.imports_utils import ImportsUtils

from .tracking_backend import TrackingBackend


class TrackingManager:
    """
    Gestionnaire de tracking indépendant du backend utilisé.

    Cette classe fournit les outils nécessaires pour gérer
    le cycle de vie d'un tracking.

    Le backend utilisé est injecté afin de masquer
    l'implémentation technique (MLflow, base de données, etc.).
    """

    @classmethod
    def create(cls) -> "TrackingManager":
        """
        Crée une instance de TrackingManager avec le backend
        défini dans la configuration du projet.

        Returns
        -------
        TrackingManager
            Gestionnaire de tracking configuré.
        """

        implementations_config = ConfigManager(
            "config/implementations.yaml"
        )

        mapping_config = ConfigManager(
            "config/mappings/tracking.yaml"
        )

        backend_name = implementations_config.get(
            "tracking.backend"
        )

        backend_module = mapping_config.get(
            f"{backend_name}.module"
        )

        backend_class_name = mapping_config.get(
            f"{backend_name}.class"
        )

        backend_class = ImportsUtils.get_class(
            backend_module,
            backend_class_name,
        )
        
        return cls(
            backend_class()
        )


    def __init__(
        self,
        backend: TrackingBackend,
    ) -> None:
        """
        Initialise le gestionnaire de tracking.

        Parameters
        ----------
        backend :
            Implémentation concrète du système de tracking.
        """

        self.backend = backend

    def initialize_experiment(
        self
    ) -> None:
        """
        Démarre une session de tracking.

        Parameters
        ----------
        run_name :
            Nom de l'expérience suivie.
        """

        self.backend.initialize_experiment()

    def start_run(
        self,
        run_name: str,
    ) -> None:
        """
        Démarre une session de tracking.

        Parameters
        ----------
        run_name :
            Nom de l'expérience suivie.
        """

        self.backend.start_run(
            run_name
        )


    def params(
        self,
        params: dict[str, Any],
    ) -> None:
        """
        Enregistre les paramètres d'une expérience.

        Parameters
        ----------
        params :
            Paramètres utilisés pendant l'expérience.
        """

        self.backend.log_params(
            params
        )


    def metrics(
        self,
        metrics: dict[str, float],
    ) -> None:
        """
        Enregistre les métriques d'une expérience.

        Parameters
        ----------
        metrics :
            Résultats mesurés.
        """

        self.backend.log_metrics(
            metrics
        )


    def artifact(
        self,
        artifact_path: str,
    ) -> None:
        """
        Enregistre un artefact associé à une expérience.

        Parameters
        ----------
        artifact_path :
            Chemin vers l'artefact.
        """

        self.backend.log_artifact(
            artifact_path
        )


    def end_run(
        self,
    ) -> None:
        """
        Termine la session de tracking.
        """

        self.backend.end_run()