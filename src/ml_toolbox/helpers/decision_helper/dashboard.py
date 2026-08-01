from pathlib import Path

from loaders.metrics_loader import MetricsLoader

from views.metrics_view import MetricsView


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

        metrics = MetricsLoader(
            self.report_path
        ).load()

        MetricsView(
            metrics,
            self.report_path,
        ).show()