# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from abc import ABC, abstractmethod
from typing import Any


class ModelPersistenceBackend(ABC):
    """
    Interface définissant les opérations de persistance.
    """

    @abstractmethod
    def save(
        self,
        model: Any,
        model_id: str
    ) -> None:
        """
        Sauvegarde un objet.

        Parameters
        ----------
        model :
            Objet à sauvegarder.

        path :
            Chemin de sauvegarde.
        """
        pass

    @abstractmethod
    def load(
        self,
        model_id: str,
    ) -> Any:
        """
        Charge un objet.

        Parameters
        ----------
        path :
            Chemin du fichier sauvegardé.

        Returns
        -------
        Any
            Objet chargé.
        """
        pass
    
    @abstractmethod
    def exists(
        self,
        model_id: str,
    ) -> Any:
        """
        Verifie l'existence d'un model.

        Parameters
        ----------
        path :
            Chemin du fichier sauvegardé.

        Returns
        -------
        Any
            Objet chargé.
        """
        pass

    @abstractmethod
    def list_models(
        self
    ) -> Any:
        """
        Retourne la liste des models enregistrés.

        Parameters
        ----------

        Returns
        -------
        Any
            Objet chargé.
        """
        pass
    
    @abstractmethod
    def find_latest(
        self
    ) -> Any:
        """
        Retourne la dernière version générée.

        Parameters
        ----------

        Returns
        -------
        Any
            Objet chargé.
        """
        pass