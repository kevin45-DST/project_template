# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from abc import ABC, abstractmethod
from typing import Any


class EvaluationBackend(ABC):
    """
    Interface définissant le contrat d'un backend d'évaluation.

    Un backend d'évaluation fournit l'implémentation technique permettant
    d'évaluer un modèle entraîné sur un jeu de données.

    Le framework utilise cette interface afin de rester indépendant de la
    bibliothèque de Machine Learning utilisée.

    Chaque implémentation doit retourner les métriques calculées ainsi que
    la matrice de confusion associée à l'évaluation.
    """

    @abstractmethod
    def evaluate(
        self,
    ) -> dict[str, Any]:
        """
        Évalue le modèle associé au backend.

        Returns
        -------
        dict[str, Any]
            Résultats de l'évaluation, comprenant notamment les métriques
            calculées et la matrice de confusion.
        """
        pass