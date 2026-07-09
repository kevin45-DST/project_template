from typing import Any

from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    MaxAbsScaler,
    Normalizer,
)


class BasicScaling:
    """
    Méthodes de mise à l'échelle (scaling) des données.

    Ces méthodes permettent d'adapter les variables à une même échelle afin
    d'améliorer les performances de nombreux algorithmes de Machine Learning.

    Toutes les méthodes retournent :

        (X_transformé, scaler)

    Le scaler retourné doit être réutilisé pour transformer les données de
    validation, de test et de production.
    """

    @staticmethod
    def standard(
        X: Any,
    ) -> tuple[Any, StandardScaler]:
        """
        Standardisation des données.

        Transformation :
            moyenne = 0
            écart-type = 1

        À utiliser lorsque :
        - les variables suivent une distribution proche d'une loi normale
        - utilisation de SVM
        - régression logistique
        - réseaux de neurones
        - PCA
        - K-Means

        Avantages :
        - méthode la plus utilisée
        - adaptée à de nombreux algorithmes

        Inconvénients :
        - sensible aux valeurs aberrantes
        """

        scaler = StandardScaler()

        return (
            scaler.fit_transform(X),
            scaler,
        )

    @staticmethod
    def min_max(
        X: Any,
        feature_range: tuple[int, int] = (0, 1),
    ) -> tuple[Any, MinMaxScaler]:
        """
        Normalisation Min-Max.

        Ramène toutes les variables dans un intervalle donné
        (par défaut [0 ; 1]).

        À utiliser lorsque :
        - réseaux de neurones
        - données bornées
        - comparaison directe entre variables

        Avantages :
        - conserve la forme de la distribution
        - simple à interpréter

        Inconvénients :
        - très sensible aux valeurs aberrantes
        """

        scaler = MinMaxScaler(
            feature_range=feature_range,
        )

        return (
            scaler.fit_transform(X),
            scaler,
        )

    @staticmethod
    def robust(
        X: Any,
    ) -> tuple[Any, RobustScaler]:
        """
        Standardisation robuste.

        Utilise la médiane et l'IQR (écart interquartile).

        À utiliser lorsque :
        - nombreuses valeurs aberrantes
        - distributions asymétriques

        Avantages :
        - peu sensible aux outliers
        - très robuste

        Inconvénients :
        - moins adapté lorsque les données sont déjà bien distribuées
        """

        scaler = RobustScaler()

        return (
            scaler.fit_transform(X),
            scaler,
        )

    @staticmethod
    def max_abs(
        X: Any,
    ) -> tuple[Any, MaxAbsScaler]:
        """
        Mise à l'échelle par valeur absolue maximale.

        Les données sont ramenées dans [-1 ; 1].

        À utiliser lorsque :
        - matrices creuses (sparse)
        - NLP
        - très grands jeux de données clairsemés

        Avantages :
        - conserve les zéros
        - adapté aux matrices sparse

        Inconvénients :
        - sensible aux valeurs extrêmes
        """

        scaler = MaxAbsScaler()

        return (
            scaler.fit_transform(X),
            scaler,
        )

    @staticmethod
    def l2_normalization(
        X: Any,
    ) -> tuple[Any, Normalizer]:
        """
        Normalisation L2.

        Chaque observation est ramenée à une norme égale à 1.

        À utiliser lorsque :
        - calcul de similarité cosinus
        - NLP
        - clustering
        - KNN

        Avantages :
        - indépendante de l'amplitude des observations
        - idéale pour les mesures de similarité

        Inconvénients :
        - ne conserve pas les amplitudes d'origine
        """

        scaler = Normalizer(
            norm="l2",
        )

        return (
            scaler.fit_transform(X),
            scaler,
        )

    @staticmethod
    def l1_normalization(
        X: Any,
    ) -> tuple[Any, Normalizer]:
        """
        Normalisation L1.

        Chaque observation est ramenée à une norme L1 égale à 1.

        À utiliser lorsque :
        - données très creuses
        - certains traitements NLP

        Avantages :
        - favorise les représentations creuses

        Inconvénients :
        - moins utilisée que la norme L2
        """

        scaler = Normalizer(
            norm="l1",
        )

        return (
            scaler.fit_transform(X),
            scaler,
        )