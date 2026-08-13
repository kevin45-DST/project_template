# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from pathlib import Path
from typing import Any

from config.config_manager import ConfigManager
from src.ml_toolbox.transversal.persistence.model_persistence_backend import (
    ModelPersistenceBackend,
)
from src.utils.imports_utils import ImportsUtils


class ModelPersistenceManager:
    """
    Gestionnaire de persistance indépendant
    de l'implémentation utilisée.
    """
    
    @classmethod
    def create(
        cls,
    ) -> "ModelPersistenceManager":
        """
        Crée un gestionnaire de persistance configuré.

        Returns
        -------
        ModelPersistenceManager
            Gestionnaire de persistance configuré.
        """

        persistence_config = ConfigManager(
            "config/mappings/persistence.yaml"
        )
        
        project_config = ConfigManager(
            "config/project.yaml"
        )
        
        persistence_type = project_config.get("model.persistence.type")

        backend_module = persistence_config.get(
            f"{persistence_type}.module"
        )

        backend_class_name = persistence_config.get(
            f"{persistence_type}.class"
        )
        
        backend_class = ImportsUtils.get_class(
            backend_module,
            backend_class_name,
        )

        backend = backend_class()

        return cls(
            backend=backend,
        )

    def __init__(
        self,
        backend: ModelPersistenceBackend
    ) -> None:
        """
        Initialise le gestionnaire de persistance.

        Parameters
        ----------
        backend :
            Implémentation de persistance utilisée.

        storage_path :
            Dossier racine de stockage.
        """

        self.backend = backend

    def save(
        self,
        model: Any,
        model_id: str,
    ) -> None:
        """
        Sauvegarde un modèle.

        Parameters
        ----------
        model :
            Modèle à sauvegarder.

        model_id :
            Identifiant logique du modèle.
        """

        self.backend.save(
            model,
            model_id
        )

    def load(
        self,
        model_id: str,
    ) -> Any:
        """
        Charge un modèle.

        Parameters
        ----------
        model_id :
            Identifiant logique du modèle.

        Returns
        -------
        Any
            Modèle chargé.
        """

        return self.backend.load(model_id)

    def exists(
        self,
        model_id: str,
    ) -> bool:
        """
        Vérifie l'existence d'un modèle.

        Parameters
        ----------
        model_id :
            Identifiant logique du modèle.

        Returns
        -------
        bool
            True si le modèle existe.
        """

        return self.backend.exists(model_id)

    def list_models(
        self,
    ) -> list[str]:
        """
        Liste les modèles disponibles.

        Returns
        -------
        list[str]
            Liste des identifiants disponibles.
        """

        return [
            item.name
            for item in self.backend.list_models()
        ]

    def find_latest(
        self
    ) -> Path | None:
        """
        Recherche la dernière version d'un modèle.

        Parameters
        ----------
        model_id :
            Identifiant logique du modèle.

        Returns
        -------
        Path | None
            Chemin du dernier modèle trouvé.
        """

        last_model = self.backend.find_latest()

        if not last_model:
            return None

        return last_model