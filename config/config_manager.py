from pathlib import Path
import yaml


class ConfigManager:
    """
    Gestionnaire centralisé de configuration.

    Les valeurs sont chargées depuis des fichiers YAML.
    Les accès se font via des clés séparées par des points.

    Exemple:
    
    config.get("models.path")
    config.get("training.cv")
    """

    def __init__(
        self,
        config_path: str | Path,
    ) -> None:
        """
        Initialise le gestionnaire de configuration.

        Parameters
        ----------
        config_path : str | Path
            Chemin vers le fichier YAML contenant la configuration.
        """
        self.config_path = Path(config_path)

        with open(
            self.config_path,
            encoding="utf-8",
        ) as file:

            self.config = yaml.safe_load(file)


    def get(
        self,
        key: str,
    ):
        """
        Récupère une valeur de configuration.

        Parameters
        ----------
        key : str
            Chemin de la clé.
            Exemple :
            "models.path"

        Returns
        -------
        Any
            Valeur associée.
        """
        try:
            value = self.config

            for item in key.split("."):
                value = value[item]

            return value
        except:
            return ""