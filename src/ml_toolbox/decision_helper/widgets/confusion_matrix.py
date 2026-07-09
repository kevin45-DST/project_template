import pandas as pd
import streamlit as st


class ConfusionMatrix:

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