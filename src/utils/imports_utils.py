# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import importlib

class ImportsUtils:
    """Utilitaires liés aux imports dynamiques."""

    @staticmethod
    def get_class(
        module_path: str,
        class_name: str,
    ):
        """
        Charge dynamiquement une classe depuis son module.

        Parameters
        ----------
        module_path :
            Chemin Python du module.

        class_name :
            Nom de la classe à charger.

        Returns
        -------
        type
            Classe chargée dynamiquement.
        """

        module = importlib.import_module(module_path)

        return getattr(
            module,
            class_name,
        )
            
            