# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from pathlib import Path
import os

import streamlit as st

from src.ml_toolbox.helpers.decision_helper.dashboard import Dashboard


st.set_page_config(
    page_title="Decision Helper",
    layout="wide",
)

Dashboard(
    Path(
        os.environ["DECISION_HELPER_REPORT_PATH"]
    )
).run()