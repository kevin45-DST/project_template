from pathlib import Path

import streamlit as st
import pandas as pd

from widgets.confusion_matrix import ConfusionMatrix
from widgets.metric_table import MetricTable

import sys
sys.path.append(str(Path(__file__).resolve().parent))
from loaders.metrics_loader import MetricsLoader


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
    ) -> None:

        self.metrics = metrics
        self.report_path = report_path

    def show(self):

        st.title("Decision Helper")

        MetricTable(
            self.metrics,
            self.report_path,
        ).show()

        self._handle_events()

    def _handle_events(self):

        selected_view = st.session_state.get(
            "selected_view"
        )

        if selected_view is None:
            return

        run_id = st.session_state.get(
            "selected_run"
        )
        
        if (
            selected_view is None
            or run_id is None
        ):
            return

        loader = MetricsLoader(
            self.report_path
        )

        if selected_view == "confusion":

            matrix = loader.load_confusion_matrix(
                run_id
            )

            ConfusionMatrix.show(
                matrix,
                run_id
            )

        st.session_state["selected_view"] = None