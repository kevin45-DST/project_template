# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import pandas as pd
import streamlit as st


class ConfusionMatrix:
    
    """
    Composant de visualisation d'une matrice de confusion.

    Cette classe transforme une matrice de confusion persistée dans un
    rapport en représentation exploitable dans l'interface Streamlit.

    Elle permet au Data Scientist d'analyser la répartition des prédictions
    par classe.

    Cette classe ne calcule pas la matrice de confusion.
    Celle-ci est produite lors de l'évaluation du modèle.
    """

    @staticmethod
    @st.dialog("Confusion Matrix")
    def show(
        matrix: dict,
        label: str
    ) -> None:
        """
        Affiche une matrice de confusion dans une boîte de dialogue.

        Parameters
        ----------
        matrix : dict
            Données de la matrice de confusion, comprenant les classes
            et les valeurs de la matrice.

        label : str
            Nom du modèle ou du résultat affiché dans le titre.
        """
        labels = matrix["classes"]

        dataframe = pd.DataFrame(
            matrix["matrix"],
            index=labels,
            columns=labels,
        )

        st.subheader(label)

        st.dataframe(
            dataframe,
            use_container_width=True,
        )