from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split

@dataclass(slots=True)
class Dataset:
    """
    Représente un dataset intégré au pipeline Machine Learning.

    Cette classe constitue le sas d'entrée des données dans le framework.
    Elle prépare la structure nécessaire aux différentes étapes du cycle
    de vie Machine Learning en séparant les données d'apprentissage et
    d'évaluation.

    Son rôle est de fournir un contrat commun aux composants suivants :

    - PreprocessingPipeline ;
    - SearchPipeline ;
    - TrainingPipeline.

    Lors de sa création, elle réalise :

    - l'identification du dataset ;
    - la séparation des variables explicatives et de la cible ;
    - le découpage train/test ;
    - la conservation des ensembles nécessaires aux phases suivantes.

    Cette classe ne réalise aucune transformation des données.

    Les traitements tels que :

    - nettoyage ;
    - gestion des valeurs manquantes ;
    - encodage ;
    - normalisation ;
    - sélection de variables ;
    - équilibrage des classes ;

    sont délégués aux composants spécialisés du framework.

    Attributes
    ----------
    name : str
        Nom du dataset.

    x_train : pd.DataFrame
        Variables explicatives destinées à l'entraînement.

    x_test : pd.DataFrame
        Variables explicatives destinées à l'évaluation.

    y_train : pd.Series
        Variables cibles associées aux données d'entraînement.

    y_test : pd.Series
        Variables cibles associées aux données de test.
    """

    name: str

    x_train: pd.DataFrame
    x_test: pd.DataFrame

    y_train: pd.Series
    y_test: pd.Series
    
    def __init__(
        self,
        name: str,
        x: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2,
        random_state: int = 42,
        stratify: bool = True,
    ) -> None:
        """
        Initialise un dataset et réalise la séparation train/test.

        Parameters
        ----------
        name : str
            Nom du dataset.

        x : pd.DataFrame
            Variables explicatives du dataset.

        y : pd.Series
            Variable cible à prédire.

        test_size : float, optional
            Proportion des données réservées au jeu de test.

        random_state : int, optional
            Graine aléatoire utilisée pour garantir la reproductibilité
            du découpage.

        stratify : bool, optional
            Indique si le découpage doit conserver la distribution des classes.
            Recommandé pour les problèmes de classification.

        Notes
        -----
        Le dataset généré contient quatre sous-ensembles :

        - x_train ;
        - x_test ;
        - y_train ;
        - y_test.
        """
        
        self.name = name

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            x,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=y if stratify else None,
        )

    @property
    def n_features(self) -> int:
        """
        Nombre de variables explicatives utilisées par le modèle.

        Returns
        -------
        int
            Nombre de colonnes présentes dans les données d'entraînement.
        """
        return self.x_train.shape[1]

    @property
    def n_train_samples(self) -> int:
        """
        Nombre d'observations utilisées pour l'entraînement.

        Returns
        -------
        int
            Taille du jeu de données d'entraînement.
        """
        return len(self.x_train)

    @property
    def n_test_samples(self) -> int:
        """
        Nombre d'observations utilisées pour l'évaluation.

        Returns
        -------
        int
            Taille du jeu de données de test.
        """
        return len(self.x_test)

    @property
    def n_samples(self) -> int:
        """
        Nombre total d'observations du dataset.

        Returns
        -------
        int
            Nombre d'observations avant séparation train/test.
        """
        return self.n_train_samples + self.n_test_samples

    def summary(self) -> dict:
        """
        Retourne les informations principales du dataset.

        Ce résumé fournit les caractéristiques générales nécessaires au suivi
        d'une expérimentation ou à l'affichage dans un outil d'analyse.

        Returns
        -------
        dict
            Informations contenant :

            - nom du dataset ;
            - nombre total d'échantillons ;
            - tailles des jeux train et test ;
            - nombre de variables explicatives.
        """

        return {
            "name": self.name,
            "n_samples": self.n_samples,
            "n_train": self.n_train_samples,
            "n_test": self.n_test_samples,
            "n_features": self.n_features,
        }