# Racine projet pour imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.ml_toolbox.decision_helper.launcher import Launcher
from config.config_manager import ConfigManager


class DecisionHelper:
    
    """
    Point d'entrée principal de l'outil d'aide à la décision.

    Le DecisionHelper fournit une interface permettant au Data Scientist
    d'analyser les résultats produits par les pipelines d'entraînement.

    Il charge la configuration du framework afin de récupérer l'emplacement
    des rapports générés, puis initialise l'interface utilisateur.

    Le DecisionHelper ne réalise pas :

    - l'entraînement des modèles ;
    - la recherche d'hyperparamètres ;
    - le calcul des métriques ;
    - la sélection automatique du meilleur modèle ;
    - le suivi MLOps.

    Son rôle est de faciliter l'analyse et la comparaison des résultats
    grâce à une interface de visualisation.

    Examples
    --------
    >>> helper = DecisionHelper()
    >>> helper.run()
    """

    def __init__(
        self,
    ) -> None:
        config = ConfigManager(
                "config/paths.yaml"
                )
        report_path = config.get(
                "reports.search"
                )
        self.report_path = Path(report_path)

    def run(self) -> None:

        launcher = Launcher(
            self.report_path,
        )

        launcher.run()
        
if __name__ == "__main__":

    helper = DecisionHelper()

    helper.run()