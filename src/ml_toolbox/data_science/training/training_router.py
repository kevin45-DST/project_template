# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from config.config_manager import ConfigManager
from src.utils.imports_utils import ImportsUtils


class TrainingRouter:
    """
    Routeur permettant de résoudre le backend d'entraînement
    adapté à un modèle donné.

    Le routeur masque la technologie utilisée pour entraîner
    un modèle (Scikit-learn, XGBoost, PyTorch, etc.).

    La résolution est réalisée à partir des fichiers de
    configuration :
    - models.yaml : définition des modèles disponibles
    - training.yaml : mapping des backends d'entraînement
    """

    def resolve(
        self,
        model_name: str,
        **model_parameters
    ) -> dict:
        """
        Résout l'implémentation du backend associée
        à un modèle.

        Parameters
        ----------
        model_name :
            Nom du modèle défini dans le mapping.

        Returns
        -------
        TrainingBackend
            Backend d'entraînement configuré.
        """
        
        models_config = ConfigManager(
            "config/mappings/models.yaml"
        )

        model_config = models_config.get(
            f"models.{model_name}"
        )

        if model_config is None:
            raise ValueError(
                f"Modèle inconnu : {model_name}"
            )
        
        model_module = model_config.get(
            "module"
        )
        
        model_class_name = model_config.get(
            "class"
        )
        
        model_backend = model_config.get(
            "backend"
        )
        
        model = (
            ImportsUtils.get_class(
                model_module,
                model_class_name
            )
        )

        return {
            "model":model(**model_parameters),
            "backend_name":model_backend
            }