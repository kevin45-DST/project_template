# Copyright © 2026 Kévin DELANОUE

# License: see LICENSE

from typing import Any

from sklearn.model_selection import GridSearchCV

from src.ml_toolbox.data_science.training.training_router import TrainingRouter


class GridCVStrategy:
    """
    Stratégie de recherche de modèle basée sur GridSearchCV.

    Cette stratégie explore systématiquement les combinaisons de paramètres
    définies dans une grille afin d'identifier la meilleure configuration
    selon un ou plusieurs critères d'évaluation.

    La stratégie est utilisée exclusivement dans le cadre de la recherche
    locale du meilleur modèle. Elle ne participe pas directement à
    l'entraînement du modèle destiné à la production.

    Parameters
    ----------
    model : Any
        Modèle compatible avec l'API scikit-learn.

    param_grid : dict[str, Any]
        Grille des hyperparamètres à explorer.

    scoring : str
        Métrique utilisée pour comparer les différentes configurations.

    cv : int, default=5
        Nombre de folds utilisés pour la validation croisée.

    n_jobs : int, default=-1
        Nombre de processus utilisés en parallèle par GridSearchCV.

    Attributes
    ----------
    best_model : Any | None
        Meilleur estimateur identifié après la recherche.

    best_params : dict[str, Any] | None
        Meilleure combinaison de paramètres identifiée.

    best_score : float | None
        Meilleur score obtenu lors de la validation croisée.

    """

    def __init__(
        self,
        model_name: Any,
        param_grid: dict[str, Any],
        scoring: str,
        cv: int = 5,
        n_jobs: int = -1,
    ) -> None:
        """
        Initialise la stratégie de recherche GridCV.

        Parameters
        ----------
        model :
            Modèle à explorer.

        param_grid :
            Grille des hyperparamètres à tester.

        scoring :
            Métrique utilisée pour comparer les configurations.

        cv :
            Nombre de folds de validation croisée.

        n_jobs :
            Nombre de processus utilisés en parallèle.
        """
        
        router = TrainingRouter()

        resolution = router.resolve(
            model_name=model_name,
        )

        self.model = resolution["model"]

        self.param_grid = param_grid
        self.scoring = scoring
        self.cv = cv
        self.n_jobs = n_jobs

        self.best_model: Any
        self.best_params: dict[str, Any]
        self.best_score: float
        self.best_fit_time: float

    def search(
        self,
        X_train: Any,
        y_train: Any,
    ):
        """
        Exécute la recherche des meilleurs hyperparamètres.

        La recherche est réalisée exclusivement sur les données
        d'entraînement afin de préserver le jeu de test pour
        l'évaluation finale.

        Parameters
        ----------
        X_train :
            Variables explicatives du jeu d'entraînement.

        y_train :
            Variable cible du jeu d'entraînement.

        Returns
        -------
        Any
            Meilleur estimateur identifié par GridSearchCV.
        """

        search = GridSearchCV(
            estimator=self.model,
            param_grid=self.param_grid,
            scoring=self.scoring,
            cv=self.cv,
            n_jobs=self.n_jobs,
        )

        search.fit(X_train, y_train)

        self.best_model = search.best_estimator_
        self.best_params = search.best_params_
        self.best_score = search.best_score_
        self.best_fit_time = search.cv_results_["mean_fit_time"][search.best_index_]