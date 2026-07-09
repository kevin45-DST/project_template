import streamlit as st
import pandas as pd

from pathlib import Path


class MetricTable:

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

                    st.session_state["selected_run"] = row["label"]
                    st.session_state["selected_view"] = "confusion"