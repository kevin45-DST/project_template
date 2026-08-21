# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from pathlib import Path

from config.config_manager import ConfigManager
from src.ml_toolbox.transversal.logs.log_collector.log_collector_manager import LogCollectorManager
from src.ml_toolbox.transversal.reporting import report_manager
from src.ml_toolbox.mlops.tracking.tracking_manager import TrackingManager


class TrackingPipeline:
    """
    Pipeline responsable du suivi des runs non encore trackés.

    Cette classe recherche les runs présents dans le registre global et
    identifie ceux qui ne possèdent pas encore de statut de tracking.

    Pour chaque run à tracker, elle :

    1. met à jour son statut de tracking ;
    2. démarre un run auprès du backend de tracking ;
    3. enregistre les métriques ;
    4. enregistre les artefacts ;
    5. met à jour le statut final du run.

    En cas d'erreur, le statut du run est marqué comme ``failed`` et le
    message de l'exception est enregistré dans son registre.

    Le backend de tracking est fourni par ``TrackingManager``.
    """

    def __init__(self):
        """
        Initialise le pipeline de tracking.
        """
        self.tracking_manager = TrackingManager.create()
        
        self.logger = LogCollectorManager()
        
    def get_runs_to_track(self):
        """
        Identifie les runs qui doivent encore être trackés.

        La méthode compare le statut de tracking présent dans le registre
        global et le registre local de chaque run.

        Les incohérences entre les deux registres sont signalées dans le
        registre local du run.

        Returns
        -------
        list[str]
            Identifiants des runs ne possédant pas encore de statut de
            tracking.
        """
        runs_to_track = []
        
        report_mng_runs = report_manager.ReportManager("")
    
        runs = report_mng_runs.get_runs_registry()
        
        self.logger.info(
            message="Début de la collecte des runs à tracker",
            logger=self.__class__.__name__,
            )

        for run_global in runs["runs"]:

            report_mng_run = report_manager.ReportManager(run_id=run_global["run_id"])
            
            run_local = report_mng_run.get_run_registry()
            
            self.logger.debug(
                message="Analyse du run",
                run_id=run_global["run_id"],
                logger=self.__class__.__name__,
                context={"run_global":run_global, "run_local":run_local}
                )

            if "tracking_status" not in run_global and "tracking_status" not in run_local:
                runs_to_track.append(
                    run_global["run_id"]
                )
            elif "tracking_status" not in run_global and "tracking_status" in run_local:
                message = "Tracking_status absent du registry global, mais présent dans le registry local"
                # Incohérence -> ajout d'un warning
                report_mng_run.update_run_info(info_name="tracking_warning_message", 
                                           info_value=message)
                self.logger.warning(
                    message=message,
                    run_id=run_global["run_id"],
                    logger=self.__class__.__name__,
                    )
            elif "tracking_status" in run_global and "tracking_status" not in run_local:
                message = "Tracking_status absent du registry local, mais présent dans le registry global"
                # Incohérence -> ajout d'un warning
                report_mng_run.update_run_info(info_name="tracking_warning_message", 
                                           info_value=message)
                self.logger.warning(
                    message=message,
                    run_id=run_global["run_id"],
                    logger=self.__class__.__name__,
                    )
            elif run_global["tracking_status"] != run_local["tracking_status"]:
                message = f"Incohérence du tracking_status local ({run_local['tracking_status']})/global ({run_global['tracking_status']})"
                # Incohérence -> ajout d'un warning
                report_mng_run.update_run_info(info_name="tracking_warning_message", 
                                           info_value=message)
                self.logger.warning(
                    message=message,
                    run_id=run_global["run_id"],
                    logger=self.__class__.__name__,
                    )
                        
                        
        self.logger.info(
            message="Fin de la collecte des runs à tracker",
            logger=self.__class__.__name__,
            )
        return runs_to_track

    def run(self):
        """
        Tracke les runs en attente.

        Chaque run est traité indépendamment. Une erreur sur un run est
        enregistrée dans son registre et n'empêche pas le traitement des
        autres runs.
        """       
        config = ConfigManager(
            "config/paths.yaml"
        )
        
        # Recherche de la liste des runs à tracker
        runs_to_track = self.get_runs_to_track()
        
        # Initialisation de l'experience
        self.tracking_manager.initialize_experiment()
        
        self.logger.info(
            message="Début du tracking des runs",
            logger=self.__class__.__name__,
            )
  
        for run_id in runs_to_track:
                    
            report_mng = report_manager.ReportManager(run_id=run_id)
            
            self.logger.info(
                message="Début du tracking",
                logger=self.__class__.__name__,
                run_id=run_id,
                context={"report":report_mng}
                )
        
            try:
                
                self.logger.debug(
                    message="Tracking en cours -> mise à jour des registry",
                    logger=self.__class__.__name__,
                    run_id=run_id
                    )
                
                # Tracking en cours -> mise à jour des registry
                report_mng.update_run_info(info_name="tracking_status", info_value="pending")
                
                self.logger.debug(
                    message="Démarrage du tracking de l'expérience",
                    logger=self.__class__.__name__,
                    run_id=run_id,
                    context={"info_name":"tracking_status", "info_value":"pending"}
                    )
                
                # Démarrage du tracking de l'expérience
                self.tracking_manager.start_run(run_id)

                # Enregistrement des paramètres
                #self.tracking_manager.params(params)

                run_path = (
                    Path(config.get("project.root_folder")) 
                    / config.get("reports.root_folder") 
                    / config.get("reports.training") 
                    / run_id
                )
                
                report = report_mng.get_run_report()

                self.logger.debug(
                    message="Enregistrement des métriques",
                    logger=self.__class__.__name__,
                    run_id=run_id
                    )
                
                # Enregistrement des métriques
                self.tracking_manager.metrics(report)
                
                self.logger.debug(
                    message="Enregistrement des artefacts",
                    logger=self.__class__.__name__,
                    run_id=run_id
                    )
                
                # Enregistrement des artefacts
                self.tracking_manager.artifact(run_path / "artifacts")
                
                self.logger.debug(
                    message="Tracking terminé -> mise à jour des registry",
                    logger=self.__class__.__name__,
                    run_id=run_id,
                    context={"info_name":"tracking_status", "info_value":"success"}
                    )
                                                
                # Tracking terminé -> mise à jour des registry
                report_mng.update_run_info(info_name="tracking_status", info_value="success")
            
            except Exception as e:
                # Tracking en echec -> mise à jour des registry
                report_mng.update_run_info(info_name="tracking_status", info_value="failed")
                # Ajout de la cause de l'exception
                report_mng.update_run_info(info_name="tracking_exception_message", info_value=str(e))
                self.logger.error(
                    message=str(e),
                    logger=self.__class__.__name__,
                    run_id=run_id,
                    context={"report":report_mng}
                    )

            finally:
                # Fin du tracking
                self.tracking_manager.end_run()
                
            self.logger.info(
                message="Fin du tracking",
                logger=self.__class__.__name__,
                run_id=run_id
                )
        
        self.logger.info(
            message="Fin du tracking des runs",
            logger=self.__class__.__name__,
            )