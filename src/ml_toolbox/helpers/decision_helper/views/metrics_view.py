# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from pathlib import Path

import streamlit as st
import pandas as pd

from src.ml_toolbox.helpers.decision_helper.widgets.confusion_matrix import ConfusionMatrix
from src.ml_toolbox.helpers.decision_helper.widgets.metric_table import MetricTable

import sys
sys.path.append(str(Path(__file__).resolve().parent))
from src.ml_toolbox.helpers.decision_helper.loaders.metrics_loader import MetricsLoader


class MetricsView:

    """
    Vue principale d'affichage des métriques du DecisionHelper.

    Cette classe gère la présentation des résultats disponibles au Data
    Scientist.

    Elle permet :

    - l'affichage du tableau des métriques ;
    - la gestion des interactions utilisateur ;
    - l'ouverture des visualisations complémentaires.

    Les données affichées proviennent des rapports générés par les pipelines.
    La vue ne réalise aucune analyse métier des performances.
    """
    
    def __init__(
        self,
        metrics: pd.DataFrame,
        report_path: Path,
        run_id: str,
    ) -> None:
        """
        Initialise la vue des métriques d'un run.

        Parameters
        ----------
        metrics : pandas.DataFrame
            Métriques à afficher.

        report_path : Path
            Répertoire contenant les rapports du run courant.

        run_id : str
            Identifiant du run affiché.
        """
        self.metrics = metrics
        self.report_path = report_path
        self.run_id = run_id

    def show(self):
        """
        Affiche les métriques et les interactions disponibles pour le run.

        La vue affiche notamment le tableau des métriques et permet
        d'ouvrir les visualisations complémentaires.
        """
        st.title("Decision Helper")
        
        st.subheader(f"Run : {self.run_id}")

        MetricTable(
            self.metrics,
            self.report_path,
        ).show()

        self._handle_events()

    def _handle_events(self):
        """
        Traite les interactions utilisateur enregistrées dans la session
        Streamlit.

        Les événements permettent notamment d'afficher une matrice de
        confusion associée au modèle sélectionné.
        """
        selected_view = st.session_state.get(
            "selected_view"
        )

        if selected_view is None:
            return
        
        model_label = st.session_state.get(
            "selected_model"
        )

        if model_label is None:
            return

        loader = MetricsLoader(
            self.report_path
        )

        if selected_view == "confusion":
            
            matrix = loader.load_confusion_matrix(
                model_label
            )

            ConfusionMatrix.show(
                matrix,
                model_label,
            )

        st.session_state["selected_view"] = None