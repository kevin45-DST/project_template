from typing import Any, Dict, Optional
import numpy as np

from sklearn.inspection import permutation_importance


class GlobalInterpretation:
    """
    Toolbox d'interprétation globale des modèles de machine learning.

    Cette classe regroupe les méthodes permettant de comprendre le comportement
    global d'un modèle après entraînement.

    Objectif :
    - Identifier les variables les plus influentes
    - Comprendre la contribution globale des features
    - Comparer des modèles entre eux

    Toutes les méthodes retournent des structures de données exploitables
    (aucune visualisation n'est générée ici).
    """

    # ============================================================
    # FEATURE IMPORTANCE (modèles basés arbres)
    # ============================================================
    @staticmethod
    def feature_importance(model) -> Dict[str, Any]:
        """
        Retourne l'importance des variables pour les modèles supportant
        nativement feature_importances_ (RandomForest, XGBoost, etc.).

        Returns:
            dict:
                {
                    "feature_importances": np.array,
                    "normalized_importances": np.array
                }
        """
        if not hasattr(model, "feature_importances_"):
            raise ValueError(
                "Ce modèle ne supporte pas feature_importances_. "
                "Utiliser permutation_importance à la place."
            )

        importances = model.feature_importances_
        normalized = importances / np.sum(importances)

        return {
            "feature_importances": importances,
            "normalized_importances": normalized
        }

    # ============================================================
    # PERMUTATION IMPORTANCE (model agnostic)
    # ============================================================
    @staticmethod
    def permutation_importance(
        model,
        X,
        y,
        scoring: str = "f1_macro",
        n_repeats: int = 5,
        random_state: Optional[int] = 42
    ) -> Dict[str, Any]:
        """
        Mesure l'importance des variables en évaluant la dégradation
        des performances lorsqu'une feature est perturbée.

        Méthode indépendante du modèle.

        Returns:
            dict:
                {
                    "importances_mean": np.array,
                    "importances_std": np.array,
                    "feature_indices": np.array
                }
        """

        result = permutation_importance(
            model,
            X,
            y,
            scoring=scoring,
            n_repeats=n_repeats,
            random_state=random_state
        )

        return {
            "importances_mean": result["importances_mean"],
            "importances_std": result["importances_std"],
            "feature_indices": np.arange(X.shape[1])
        }

    # ============================================================
    # GLOBAL SHAP (optionnel, dépend installation shap)
    # ============================================================
    @staticmethod
    def shap_global(explainer) -> Dict[str, Any]:
        """
        Retourne les valeurs SHAP globales à partir d'un explainer déjà construit.

        Attention :
        - cette méthode suppose que les SHAP values ont déjà été calculées
        - elle ne construit pas l'explainer

        Returns:
            dict:
                {
                    "shap_values": np.array,
                    "base_value": float
                }
        """
        shap_values = explainer.shap_values
        base_value = getattr(explainer, "expected_value", None)

        return {
            "shap_values": shap_values,
            "base_value": base_value
        }

    # ============================================================
    # IMPORTANCE NORMALISÉE (outil utilitaire)
    # ============================================================
    @staticmethod
    def normalize(importances: np.ndarray) -> np.ndarray:
        """
        Normalise un vecteur d'importance pour obtenir des proportions.
        """
        importances = np.array(importances, dtype=float)
        total = np.sum(importances)

        if total == 0:
            return importances

        return importances / total

    # ============================================================
    # RÉSUMÉ GLOBAL SIMPLE (pour reporting interne)
    # ============================================================
    @staticmethod
    def summary(
        feature_names,
        importances: np.ndarray
    ) -> Dict[str, Any]:
        """
        Génère un résumé structuré des importances globales.

        Utile pour les reports automatiques.
        """

        importances = np.array(importances)

        sorted_idx = np.argsort(importances)[::-1]

        return {
            "ranking": [
                {
                    "feature": feature_names[i],
                    "importance": float(importances[i])
                }
                for i in sorted_idx
            ]
        }