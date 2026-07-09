from dataclasses import dataclass
import pandas as pd

@dataclass(slots=True)
class Dataset:
    """
    Représente un dataset d'entraînement.

    Cette classe encapsule les données nécessaires à l'entraînement d'un
    modèle de Machine Learning.

    Parameters
    ----------
    name :
        Nom du dataset.

    x_train :
        Variables d'entraînement.

    x_test :
        Variables de test.

    y_train :
        Labels d'entraînement.

    y_test :
        Labels de test.

    Notes
    -----
    Les données doivent être prétraitées avant la création du Dataset
    (normalisation, encodage, feature engineering...).

    Cette classe ne réalise aucun prétraitement.

    Comment utiliser
    ----------------
    >>> dataset = Dataset(
    ...     name="Dataset1",
    ...     x_train=x_train,
    ...     x_test=x_test,
    ...     y_train=y_train,
    ...     y_test=y_test,
    ... )
    """

    name: str

    x_train: pd.DataFrame
    x_test: pd.DataFrame

    y_train: pd.Series
    y_test: pd.Series

    @property
    def n_features(self) -> int:
        """
        Retourne le nombre de variables explicatives.
        """
        return self.x_train.shape[1]

    @property
    def n_train_samples(self) -> int:
        """
        Retourne le nombre d'observations d'entraînement.
        """
        return len(self.x_train)

    @property
    def n_test_samples(self) -> int:
        """
        Retourne le nombre d'observations de test.
        """
        return len(self.x_test)

    @property
    def n_samples(self) -> int:
        """
        Retourne le nombre total d'observations.
        """
        return self.n_train_samples + self.n_test_samples

    def summary(self) -> dict:
        """
        Retourne un résumé du dataset.

        Returns
        -------
        dict
            Informations principales sur le dataset.
        """

        return {
            "name": self.name,
            "n_samples": self.n_samples,
            "n_train": self.n_train_samples,
            "n_test": self.n_test_samples,
            "n_features": self.n_features,
        }