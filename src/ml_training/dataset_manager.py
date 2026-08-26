from __future__ import annotations
from typing import List
import pandas as pd
from sklearn.model_selection import train_test_split
from .dataset import Dataset


class DatasetManager:
    """
    Gestionnaire des datasets.

    Cette classe est responsable de la création et du stockage des
    différents datasets utilisés pendant les entraînements.

    Elle ne réalise aucun prétraitement.

    Responsabilités
    ----------------
    - création d'un Dataset
    - split train/test
    - stockage des datasets
    - récupération des datasets

    Elle ne réalise PAS :
    - normalisation
    - encodage
    - feature engineering

    Comment utiliser
    ----------------

    >>> manager = DatasetManager()

    >>> manager.add_dataset(
    ...     name="raw",
    ...     x=x,
    ...     y=y,
    ... )

    >>> datasets = manager.get_datasets()
    """

    def __init__(self) -> None:
        """
        Initialise le gestionnaire.
        """

        self._datasets: List[Dataset] = []

    def add_dataset(
        self,
        name: str,
        x: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2,
        random_state: int = 42,
        stratify: bool = True,
    ) -> Dataset:
        """
        Crée un Dataset puis l'ajoute au gestionnaire.

        Parameters
        ----------
        name :
            Nom du dataset.

        x :
            Variables explicatives.

        y :
            Variable cible.

        test_size :
            Taille du jeu de test.

        random_state :
            Graine aléatoire.

        stratify :
            Réalise un split stratifié si True.

        Returns
        -------
        Dataset
            Dataset créé.
        """

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=y if stratify else None,
        )

        dataset = Dataset(
            name=name,
            x_train=x_train,
            x_test=x_test,
            y_train=y_train,
            y_test=y_test,
        )

        self._datasets.append(dataset)

        return dataset

    def register(self, dataset: Dataset) -> None:
        """
        Enregistre un Dataset existant.

        Cette méthode permet d'ajouter un Dataset déjà construit
        (par exemple après un prétraitement spécifique).

        Parameters
        ----------
        dataset :
            Dataset à enregistrer.
        """

        self._datasets.append(dataset)

    def remove(self, name: str) -> None:
        """
        Supprime un dataset.

        Parameters
        ----------
        name :
            Nom du dataset.
        """

        self._datasets = [
            dataset
            for dataset in self._datasets
            if dataset.name != name
        ]

    def clear(self) -> None:
        """
        Supprime tous les datasets.
        """

        self._datasets.clear()

    def get(self, name: str) -> Dataset:
        """
        Retourne un dataset.

        Parameters
        ----------
        name :
            Nom du dataset.

        Returns
        -------
        Dataset

        Raises
        ------
        ValueError
            Si le dataset est introuvable.
        """

        for dataset in self._datasets:
            if dataset.name == name:
                return dataset

        raise ValueError(f"Dataset '{name}' not found.")

    def get_datasets(self) -> list[Dataset]:
        """
        Retourne tous les datasets.

        Returns
        -------
        list[Dataset]
        """

        return self._datasets.copy()

    @property
    def count(self) -> int:
        """
        Retourne le nombre de datasets enregistrés.
        """

        return len(self._datasets)

    @property
    def names(self) -> list[str]:
        """
        Retourne les noms des datasets.
        """

        return [dataset.name for dataset in self._datasets]