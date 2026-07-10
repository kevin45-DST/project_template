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