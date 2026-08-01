from pathlib import Path
import json
import sys

sys.path.append(
    str(Path(__file__).resolve().parents[4])
)

from config.config_manager import ConfigManager


class runRecovery:
    """
    Permet de reconstruire le registre global des expériences
    à partir des registres locaux présents dans chaque dossier
    d'expérience.
    """

    def __init__(
        self,
        runs_path: Path,
        global_registry_path: Path,
    ) -> None:
        """
        Initialise le composant de reconstruction des expériences.

        Parameters
        ----------
        runs_path : Path
            Dossier contenant les différentes expériences.

        global_registry_path : Path
            Chemin du fichier 'runs_registry.json' à reconstruire.
        """

        self.runs_path = runs_path
        self.global_registry_path = global_registry_path

    def recover(self) -> list[dict]:
        """
        Parcourt les dossiers d'expériences et récupère les informations
        contenues dans chaque fichier 'run_registry.json'.

        Returns
        -------
        list[dict]
            Liste des expériences récupérées.
        """

        runs = []

        if not self.runs_path.exists():
            return runs

        for run_dir in self.runs_path.iterdir():

            if not run_dir.is_dir():
                continue

            if not run_dir.name.startswith(
                "run_"
            ):
                continue

            registry_path = (
                run_dir
                / "run_registry.json"
            )

            if not registry_path.exists():
                continue

            run = self._load_registry(
                registry_path
            )

            if run:
                runs.append(run)

        return runs

    def rebuild_global_registry(
        self,
        runs: list[dict],
    ) -> None:
        """
        Reconstruit le fichier 'runs_registry.json'
        à partir de la liste des expériences récupérées.

        Parameters
        ----------
        runs : list[dict]
            Liste des expériences à enregistrer dans le registre global.
        """

        registry = {
            "runs": runs
        }

        self.global_registry_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.global_registry_path / "runs_registry.json",
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                registry,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def recover_and_rebuild(self) -> list[dict]:
        """
        Reconstruit le registre global des expériences.

        Cette méthode récupère les informations contenues dans les
        registres locaux de chaque expérience puis génère un nouveau
        fichier 'runs_registry.json'.

        Returns
        -------
        list[dict]
            Liste des expériences récupérées.
        """

        runs = self.recover()

        self.rebuild_global_registry(
            runs
        )

        return runs

    @staticmethod
    def _load_registry(
        registry_path: Path,
    ) -> dict | None:
        """
        Charge le registre local d'une expérience.

        Parameters
        ----------
        registry_path : Path
            Chemin vers le fichier 'run_registry.json'.

        Returns
        -------
        dict | None
            Contenu du registre si le fichier est valide,
            sinon None.
        """

        try:
            with open(
                registry_path,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except json.JSONDecodeError:
            return None
        
def main() -> None:
    
    config = ConfigManager(
            "config/paths.yaml"
        )

    training_path = Path(config.get("project.root_folder")) / config.get("reports.root_folder") / config.get("reports.training")

    recovery = runRecovery(
        runs_path = training_path,
        global_registry_path = training_path,
    )

    runs = recovery.recover_and_rebuild()

    print(
        f"{len(runs)} runs_registry restauré."
    )


if __name__ == "__main__":
    main()