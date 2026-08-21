# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from pathlib import Path
import os
import subprocess
import sys


class Launcher:
    
    """
    Lanceur de l'application utilisateur du DecisionHelper.

    Cette classe prépare l'environnement nécessaire au démarrage de
    l'application Streamlit.

    Responsabilités :

    - transmettre le chemin des rapports à l'application ;
    - démarrer le serveur Streamlit ;
    - lancer l'interface graphique du DecisionHelper.

    Cette classe ne contient aucune logique d'analyse des résultats.
    """

    def __init__(
        self,
        report_path: Path,
    ) -> None:
        """
        Initialise le lanceur du DecisionHelper.

        Parameters
        ----------
        report_path : Path
            Répertoire racine contenant les rapports à analyser.
        """
        self.report_path = report_path

    def run(self) -> None:
        """
        Démarre l'application Streamlit du DecisionHelper.

        Le chemin des rapports est transmis à l'application via la variable
        d'environnement ``DECISION_HELPER_REPORT_PATH``.
        """
        os.environ["DECISION_HELPER_REPORT_PATH"] = str(
            self.report_path
        )

        app = (
            Path(__file__).parent
            / "app.py"
        )

        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(app),
            ]
        )