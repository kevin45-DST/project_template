from typing import Any, Tuple

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.combine import SMOTETomek


class BasicBalancing:
    """
    Méthodes de rééquilibrage de base.

    Ces méthodes sont recommandées comme première approche lorsqu'on travaille
    avec des jeux de données déséquilibrés.

    Elles sont :
    - rapides
    - stables
    - largement utilisées
    - peu coûteuses en calcul

    Toutes les méthodes retournent :
        (X rééchantillonné, y rééchantillonné)
    """

    @staticmethod
    def random_undersampling(
        X: Any,
        y: Any,
        random_state: int = 42,
    ) -> Any:
        """
        Supprime aléatoirement des échantillons de la classe majoritaire.

        À utiliser lorsque :
        - le jeu de données est volumineux
        - on souhaite un baseline rapide
        - la perte d'information est acceptable

        Avantages :
        - très rapide
        - simple et stable

        Inconvénients :
        - perte d'information sur la classe majoritaire
        """

        sampler = RandomUnderSampler(random_state=random_state)
        return sampler.fit_resample(X, y)

    @staticmethod
    def random_oversampling(
        X: Any,
        y: Any,
        random_state: int = 42,
    ) -> Any:
        """
        Duplique aléatoirement les échantillons de la classe minoritaire.

        À utiliser lorsque :
        - on veut une amélioration rapide face au déséquilibre
        - le jeu de données est petit à moyen

        Avantages :
        - aucune perte d'information
        - très simple à mettre en place

        Inconvénients :
        - risque de surapprentissage dû à la duplication
        """

        sampler = RandomOverSampler(random_state=random_state)
        return sampler.fit_resample(X, y)

    @staticmethod
    def smote(
        X: Any,
        y: Any,
        random_state: int = 42,
        k_neighbors: int = 5,
    ) -> Any:
        """
        Génère des échantillons synthétiques pour la classe minoritaire.

        À utiliser lorsque :
        - on souhaite une meilleure généralisation que le sur-échantillonnage simple
        - la classe minoritaire contient suffisamment d'exemples

        Avantages :
        - pas de simple duplication
        - meilleure généralisation que le sur-échantillonnage aléatoire

        Inconvénients :
        - coût de calcul plus élevé
        - risque de génération de points bruités dans des distributions complexes
        """

        sampler = SMOTE(
            random_state=random_state,
            k_neighbors=k_neighbors,
        )
        return sampler.fit_resample(X, y)

    @staticmethod
    def smote_tomek(
        X: Any,
        y: Any,
        random_state: int = 42,
    ) -> Any:
        """
        Combine SMOTE avec le nettoyage par liens de Tomek.

        À utiliser lorsque :
        - SMOTE seul ne suffit pas
        - on souhaite améliorer la séparation entre les classes

        Avantages :
        - améliore la séparation des classes
        - réduit le chevauchement entre classes

        Inconvénients :
        - coût de calcul plus élevé
        - transformation plus agressive des données
        """

        sampler = SMOTETomek(random_state=random_state)
        return sampler.fit_resample(X, y)