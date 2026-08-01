import json
from pathlib import Path

import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay


class imageUtils:
    
    def save_confusion_matrix_from_json(
        self,
        json_path: Path
    ) :
        """
        Génère une image de matrice de confusion à partir
        d'un fichier JSON.

        Parameters
        ----------
        json_path :
            Chemin du fichier JSON contenant la matrice.

        output_path :
            Chemin du fichier image à générer.
        """

        with open(
            json_path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        classes = data["classes"]

        matrix = np.array(
            data["matrix"]
        )

        display = ConfusionMatrixDisplay(
            confusion_matrix=matrix,
            display_labels=classes,
        )

        return display