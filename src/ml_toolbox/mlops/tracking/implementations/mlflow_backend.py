# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from pathlib import Path
from typing import Any

import mlflow

from config.config_manager import ConfigManager

from ..tracking_backend import TrackingBackend


class MLFlowBackend(TrackingBackend):
    """
    Implémentation du tracking utilisant MLflow.

    Cette classe adapte l'API MLflow au contrat défini
    par TrackingBackend.

    Le reste du framework ne connaît pas MLflow.
    """
    
    def __init__(
        self
    ):
        
        self.load_config()
        
        self.experiment_id = None

        mlflow.set_tracking_uri(
            self.database_uri
        )
        
    def load_config(self) -> None:
                
        paths_config = ConfigManager(
            "config/paths.yaml"
        )
        
        project_config = ConfigManager(
            "config/project.yaml"
        )
        
        project_root_folder = Path(paths_config.get('project.root_folder'))
        
        mlflow_root_folder = (
                        project_root_folder / 
                        paths_config.get('tracking.root_folder') /
                        paths_config.get('tracking.mlflow.root_folder')
                      )

        artifact_path = mlflow_root_folder / paths_config.get('tracking.mlflow.artifacts')
        
        artifact_path.mkdir(parents=True, exist_ok=True)

        self.experiment_name = project_config.get("project.name")
        self.database_uri = (
                            f"{project_config.get('mlflow.backend.type')}"
                            ":///"
                            f"{mlflow_root_folder / project_config.get('mlflow.backend.name')}"
                            )
        self.artifact_location = "file:///" + str(artifact_path).replace("\\", "/")

        
    def initialize_experiment(
        self
    ) -> None:
        
        experiment = mlflow.get_experiment_by_name(self.experiment_name)

        if experiment is None:
            self.experiment_id = mlflow.create_experiment(
                name=self.experiment_name,
                artifact_location=self.artifact_location,
            )
        else:
            self.experiment_id = experiment.experiment_id      

    def start_run(
        self,
        run_name: str,
    ) -> None:

        mlflow.start_run(
            experiment_id=self.experiment_id,
            run_name=run_name
        )


    def log_params(
        self,
        params: dict[str, Any],
    ) -> None:

        mlflow.log_params(
            params
        )


    def log_metrics(
        self,
        metrics: dict[str, float],
    ) -> None:

        mlflow.log_metrics(
            metrics
        )


    def log_artifact(
        self,
        path: str,
    ) -> None:

        mlflow.log_artifact(
            path
        )


    def end_run(
        self,
    ) -> None:

        mlflow.end_run()