from pathlib import Path
import os

import streamlit as st

from dashboard import Dashboard


st.set_page_config(
    page_title="Decision Helper",
    layout="wide",
)

Dashboard(
    Path(
        os.environ["DECISION_HELPER_REPORT_PATH"]
    )
).run()