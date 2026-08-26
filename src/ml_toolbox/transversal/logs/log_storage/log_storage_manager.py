# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import json
from pathlib import Path
from typing import Any

from config.config_manager import ConfigManager
from src.utils.imports_utils import ImportsUtils

from .log_storage_backend import LogStorageBackend


class LogStorageManager:
    """Gère le stockage des logs via un backend."""
    
    @classmethod
    def create(cls) -> "LogStorageManager":
        """
        Crée une instance de LogStorageManager avec le backend
        défini dans la configuration du projet.
    
        Returns
        -------
        LogStorageManager
            Gestionnaire de logstorage configuré.
        """
    
        project_config = ConfigManager(
            "config/project.yaml"
        )
    
        mapping_config = ConfigManager(
            "config/mappings/logs.yaml"
        )
    
        backend_name = project_config.get(
            "logs.storage.backend"
        )
    
        backend_module = mapping_config.get(
            f"{backend_name}.module"
        )
    
        backend_class_name = mapping_config.get(
            f"{backend_name}.class"
        )
        
        backend_implementation_class = ImportsUtils.get_class(
            backend_module,
            backend_class_name,
        )
        
        return cls(
            backend_implementation_class()
        )

    def __init__(self, backend: LogStorageBackend) -> None:
        """
        Initialise le gestionnaire de stockage.

        Args:
            backend: Backend utilisé pour stocker les logs.
        """
        
        paths_config = ConfigManager(
            "config/paths.yaml"
        )
        
        self.log_directory = Path(paths_config.get("project.root_folder")) / paths_config.get("logs.root_folder")
        self.registry_path = self.log_directory / "log_storage_state.json"
        self.backend = backend
        self.offsets = self.load_registry()        

    def store(self) -> None:
        """Stocke les nouveaux logs disponibles."""

        for log_file in self.get_log_files():
            self.process_file(log_file)

    def process_file(self, log_file: Path) -> None:
        """
        Traite les nouvelles données d'un fichier de logs.

        Args:
            log_file: Fichier de logs à traiter.
        """
        file_key = str(log_file.resolve())
        current_size = log_file.stat().st_size
        offset = self.offsets.get(file_key, 0)

        # Le fichier a été tronqué ou recréé.
        if current_size < offset:
            offset = 0

        if current_size == offset:
            return

        logs = self.read_from_offset(log_file, offset)

        if not logs:
            return

        for log in logs:

            success = self.backend.store(log)

            if success:
                self.offsets[file_key] = current_size
                self.save_registry()

    def read_from_offset(
        self,
        log_file: Path,
        offset: int,
    ) -> list[dict[str, Any]]:
        """
        Lit les logs situés après un offset donné.

        Args:
            log_file: Fichier de logs à lire.
            offset: Position de départ dans le fichier.

        Returns:
            Liste des logs décodés.
        """
        logs = []

        with log_file.open("r", encoding="utf-8") as file:
            file.seek(offset)

            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    # La ligne peut être en cours d'écriture.
                    continue

        return logs

    def get_log_files(self) -> list[Path]:
        """
        Retourne les fichiers de logs disponibles.

        Returns:
            Liste des fichiers JSONL.
        """

        return sorted(self.log_directory.rglob("*.jsonl"))
    
    def load_registry(self) -> dict[str, int]:
        """Charge les offsets persistés ou initialise le fichier d'état."""
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            self.registry_path.write_text("{}", encoding="utf-8")
            return {}

        with self.registry_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save_registry(self) -> None:
        """Sauvegarde les offsets de lecture."""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        temporary_path = self.registry_path.with_suffix(".tmp")

        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(
                self.offsets,
                file,
                indent=2,
                ensure_ascii=False,
            )

        temporary_path.replace(self.registry_path)