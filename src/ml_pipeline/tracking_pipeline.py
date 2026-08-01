from asyncio import exceptions
import json
from pathlib import Path

import pandas as pd

from config.config_manager import ConfigManager
from src.ml_toolbox.reporting import report_manager
from src.ml_toolbox.mlops.tracking.tracking_manager import TrackingManager


class TrackingPipeline:


    def __init__(self):

        self.tracking_manager = TrackingManager.create()
        
    def get_runs_to_track(self):
        
        runs_to_track = []
        
        report_mng_runs = report_manager.ReportManager("")
    
        runs = report_mng_runs.get_runs_registry()

        for run_global in runs["runs"]:

            report_mng_run = report_manager.ReportManager(run_id=run_global["run_id"])
            
            run_local = report_mng_run.get_run_registry()

            if "tracking_status" not in run_global and "tracking_status" not in run_local:
                runs_to_track.append(
                    run_global["run_id"]
                )
            elif "tracking_status" not in run_global and "tracking_status" in run_local:
                # Incohérence ->x ajout d'un warning
                report_mng_run.update_run_info(info_name="tracking_warning_message", 
                                           info_value="Tracking_status absent du registry global, mais présent dans le registry local")
            elif "tracking_status" in run_global and "tracking_status" not in run_local:
                # Incohérence ->x ajout d'un warning
                report_mng_run.update_run_info(info_name="tracking_warning_message", 
                                           info_value="Tracking_status absent du registry local, mais présent dans le registry global")
            elif run_global["tracking_status"] != run_local["tracking_status"]:
                # Incohérence ->x ajout d'un warning
                report_mng_run.update_run_info(info_name="tracking_warning_message", 
                                           info_value=f"Incohérence du tracking_status local ({run_local['tracking_status']})/global ({run_global['tracking_status']})")
                        
        return runs_to_track

    def run(self):
        
        config = ConfigManager(
            "config/paths.yaml"
        )
        
        # Recherche de la liste des runs à tracker
        runs_to_track = self.get_runs_to_track()
        
        # Initialisation de l'experience
        self.tracking_manager.initialize_experiment()
  
        for run_id in runs_to_track:
        
            report_mng = report_manager.ReportManager(run_id=run_id)
        
            try:
                
                # Tracking en cours -> mise à jour des registry
                report_mng.update_run_info(info_name="tracking_status", info_value="pending")
                
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

                # Enregistrement des métriques
                self.tracking_manager.metrics(report)

                # Enregistrement des artefacts
                self.tracking_manager.artifact(run_path / "artifacts")
                
                # Tracking terminé -> mise à jour des registry
                report_mng.update_run_info(info_name="tracking_status", info_value="success")
            
            except Exception as e:
                # Tracking en echec -> mise à jour des registry
                report_mng.update_run_info(info_name="tracking_status", info_value="failed")
                # Ajout de la cause de l'exception
                report_mng.update_run_info(info_name="tracking_exception_message", info_value=str(e))

            finally:
                # Fin du tracking
                self.tracking_manager.end_run()