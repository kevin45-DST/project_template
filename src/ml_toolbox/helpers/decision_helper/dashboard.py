# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from pathlib import Path
import streamlit as st

from src.ml_toolbox.helpers.decision_helper.loaders.metrics_loader import MetricsLoader

from src.ml_toolbox.helpers.decision_helper.views.metrics_view import MetricsView


class Dashboard:
    
    """
    Orchestrateur principal du tableau de bord DecisionHelper.

    Cette classe coordonne le chargement des résultats et leur affichage
    dans l'interface utilisateur.

    Le flux exécuté est :

    1. Chargement des métriques depuis les rapports générés.
    2. Création des composants de visualisation.
    3. Affichage des informations disponibles au Data Scientist.

    Le Dashboard ne calcule aucune métrique et ne modifie aucun résultat
    d'expérimentation.
    """

    def __init__(
        self,
        report_path: Path,
    ) -> None:

        self.report_path = report_path

    def run(self) -> None:
        
        runs = MetricsLoader(
            self.report_path
        ).list_runs()

        if not runs:
            st.warning("Aucun run disponible.")
            return

        selected_run = st.sidebar.radio(
            "Runs",
            runs,
        )

        run_path = self.report_path / selected_run

        metrics = MetricsLoader(
            run_path
        ).load()

        MetricsView(
            metrics,
            run_path,
            selected_run,
        ).show()