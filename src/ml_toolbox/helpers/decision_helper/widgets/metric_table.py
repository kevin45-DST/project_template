# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import streamlit as st
import pandas as pd

from pathlib import Path


class MetricTable:
    
    """
    Composant d'affichage des métriques d'expérimentation.

    Cette classe présente les résultats des modèles sous forme de tableau
    interactif.

    Elle permet notamment :

    - de consulter les métriques disponibles ;
    - de sélectionner une expérimentation ;
    - d'afficher des informations complémentaires comme la matrice
      de confusion.

    Elle ne réalise aucune comparaison automatique ni recommandation de
    modèle.
    """

    def __init__(
        self,
        metrics: pd.DataFrame,
        report_path: Path,
    ) -> None:

        self.metrics = metrics
        self.report_path = report_path

    def show(self):

        for _, row in self.metrics.iterrows():

            c1, c2 = st.columns(
                [8,1]
            )

            with c1:

                st.write(
                    row.to_frame().T
                )

            with c2:

                if st.button(
                    "👁",
                    key=f"cm_{row['label']}",
                ):

                    st.session_state["selected_model"] = row["label"]
                    st.session_state["selected_view"] = "confusion"