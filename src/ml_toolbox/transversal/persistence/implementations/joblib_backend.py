# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from pathlib import Path
from typing import Any

import joblib

from config.config_manager import ConfigManager
from src.ml_toolbox.transversal.persistence.model_persistence_backend import (
    ModelPersistenceBackend,
)


class JoblibPersistenceBackend(ModelPersistenceBackend):
    """
    Implémentation de la persistance basée sur joblib.
    """
    
    def __init__(self):
        
        paths_config = ConfigManager(
            "config/paths.yaml"
        )
        
        project_root_folder = Path(paths_config.get("project.root_folder"))
        
        self.persistence_folder_path = (
                        project_root_folder / 
                        paths_config.get("persistence.root_folder") 
                      )
    
        self.persistence_folder_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        model: Any,
        model_id: str,
    ) -> None:
        """
        Sauvegarde un objet avec joblib.

        Parameters
        ----------
        model :
            Objet à sauvegarder.

        path :
            Chemin du fichier de sauvegarde.
        """

        joblib.dump(
            model,
            self.persistence_folder_path / f"{model_id}.joblib",
        )

    def load(
        self,
        model_id: str
    ) -> Any:
        """
        Charge un objet avec joblib.

        Parameters
        ----------
        path :
            Chemin du fichier sauvegardé.

        Returns
        -------
        Any
            Objet chargé.
        """

        return joblib.load(
            self.persistence_folder_path / f"{model_id}.joblib",
        )
        
    def exists(
        self,
        model_id: str,
    ) -> bool:
        """
        Vérifie l'existence d'un modèle.

        Parameters
        ----------
        model_id :
            Identifiant du modèle.

        Returns
        -------
        bool
            True si le modèle existe, sinon False.
        """

        return (
            self.persistence_folder_path
            / model_id
        ).is_file()

    def list_models(
        self,
    ) -> list[str]:
        """
        Retourne la liste des modèles enregistrés.

        Returns
        -------
        list[str]
            Identifiants des modèles enregistrés.
        """

        if not self.persistence_folder_path.exists():
            return []

        return [
            path.name
            for path in self.persistence_folder_path.iterdir()
            if path.is_file()
        ]

    def find_latest(
        self,
    ) -> str | None:
        """
        Retourne le dernier modèle enregistré.

        Returns
        -------
        str | None
            Identifiant du dernier modèle enregistré,
            ou None si aucun modèle n'existe.
        """

        if not self.persistence_folder_path.exists():
            return None

        models = [
            path
            for path in self.persistence_folder_path.iterdir()
            if path.is_file()
        ]

        if not models:
            return None

        latest_model = max(
            models,
            key=lambda path: path.stat().st_mtime,
        )

        return latest_model.name