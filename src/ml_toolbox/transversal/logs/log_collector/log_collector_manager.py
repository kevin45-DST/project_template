# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from config.config_manager import ConfigManager
from src.utils.numerics_utils import NumericsUtils


class LogCollectorManager:
    """Collecte et persiste les événements de log du framework.

    Les logs sont normalisés puis écrits au format JSONL.
    Le chemin de stockage est défini dans le fichier
    ``config/paths.yaml``.

    Le manager gère également la rotation des fichiers selon
    leur taille.

    Parameters
    ----------
    config_path : dans paths.yaml
    max_file_size : dans project.yaml
    
    Information
    ----------
    Les timestamp sont volontairement en UTC. 
    Il peut donc y avoir un décallage en fonction de la position géographique de la machine
    """

    def __init__(
        self
    ) -> None:
        """Initialise le collecteur de logs.

        Config
        ----------
        Log_level :
            0	DEBUG + INFO + WARNING + ERROR
            1	INFO + WARNING + ERROR
            2	WARNING + ERROR
            3	ERROR uniquement

        Raises
        ------
        FileNotFoundError
            Si le fichier de configuration n'existe pas.
        ValueError
            Si la configuration ne contient pas le chemin des logs.
        """
        paths_config = ConfigManager("config/paths.yaml")
        project_config = ConfigManager("config/project.yaml")
        log_mapping = ConfigManager("config/mappings/logs.yaml")
        
        self.log_level = project_config.get("logs.level")
        self.log_levels_mapping = log_mapping.get("log_levels")
        
        self.log_directory = Path(paths_config.get("project.root_folder")) / paths_config.get("logs.root_folder")
        
        self._max_file_size = NumericsUtils.parse_file_size(project_config.get("logs.file_size_max"))

        self.log_directory.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        level: str,
        message: str,
        *,
        logger: str | None = None,
        run_id: str | None = None,
        **context: Any,
    ) -> None:
        """Collecte et persiste un événement de log.

        Parameters
        ----------
        level : str
            Niveau du log.
        message : str
            Message à journaliser.
        logger : str | None, optional
            Nom du composant ayant produit le log.
        run_id : str | None, optional
            Identifiant du run associé au log.
        **context : Any
            Informations contextuelles supplémentaires.
        """

        # on n'ecrit que si le niveau correspond
        if level.upper() in self.log_levels_mapping[self.log_level]:
            event = self._build_event(
                level=level,
                message=message,
                logger=logger,
                run_id=run_id,
                context=context,
            )

            self._write_event(event)

    def debug(
        self,
        message: str,
        *,
        logger: str | None = None,
        run_id: str | None = None,
        context: Any = {},
    ) -> None:
        """Collecte un événement de niveau DEBUG."""
        self.log(
            "DEBUG",
            message,
            logger=logger,
            run_id=run_id,
            **context,
        )

    def info(
        self,
        message: str,
        *,
        logger: str | None = None,
        run_id: str | None = None,
        context: Any={},
    ) -> None:
        """Collecte un événement de niveau INFO."""
        self.log(
            "INFO",
            message,
            logger=logger,
            run_id=run_id,
            **context,
        )

    def warning(
        self,
        message: str,
        *,
        logger: str | None = None,
        run_id: str | None = None,
        **context: Any,
    ) -> None:
        """Collecte un événement de niveau WARNING."""
        self.log(
            "WARNING",
            message,
            logger=logger,
            run_id=run_id,
            **context,
        )

    def error(
        self,
        message: str,
        *,
        logger: str | None = None,
        run_id: str | None = None,
        **context: Any,
    ) -> None:
        """Collecte un événement de niveau ERROR."""
        self.log(
            "ERROR",
            message,
            logger=logger,
            run_id=run_id,
            **context,
        )

    @staticmethod
    def _build_event(
        *,
        level: str,
        message: str,
        logger: str | None,
        run_id: str | None,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Construit un événement de log normalisé.

        Parameters
        ----------
        level : str
            Niveau du log.
        message : str
            Message du log.
        logger : str | None
            Nom du composant émetteur.
        run_id : str | None
            Identifiant du run.
        context : dict[str, Any]
            Contexte associé à l'événement.

        Returns
        -------
        dict[str, Any]
            Événement normalisé.
        """
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level.upper(),
            **({"run_id": run_id} if run_id else {}),
            "logger": logger,
            "message": message,
            **({"context": context} if context else {})
        }

    def _write_event(self, event: dict[str, Any]) -> None:
        """Écrit un événement dans le fichier JSONL courant."""
        log_file = self._get_current_log_file()

        serialized_event = json.dumps(
            event,
            ensure_ascii=False,
            default=str,
        )

        with log_file.open("a", encoding="utf-8") as file:
            file.write(serialized_event)
            file.write("\n")

    def _get_current_log_file(self) -> Path:
        """Retourne le fichier de log courant en appliquant la rotation."""
        date_directory = self.log_directory / datetime.now().strftime("%Y-%m-%d")
        date_directory.mkdir(parents=True, exist_ok=True)

        index = 1

        while True:
            log_file = date_directory / f"log_{index:03d}.jsonl"

            if not log_file.exists():
                return log_file

            if log_file.stat().st_size < self._max_file_size:
                return log_file

            index += 1