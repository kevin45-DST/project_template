class RunFailureRecovery:
    """
    Gestion de la récupération des runs en échec.

    Cette classe archive les informations des runs failed
    puis les retire du registry afin de permettre leur
    nouveau traitement.

    Les manipulations du registry et de l'historique sont
    déléguées respectivement au ReportManager et au LogManager.
    """

    @staticmethod
    def recover() -> None:
        """
        Archive les runs en échec puis nettoie le registry.
        """

        # Récupération des runs actuellement en échec
        failed_runs = ReportManager.get_failed_runs()

        if not failed_runs:
            return

        # Archivage de l'état des runs
        LogManager.archive_run_recovery(
            failed_runs
        )

        # Suppression des informations d'échec
        ReportManager.reset_failed_runs(
            failed_runs
        )