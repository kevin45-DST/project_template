import os
import joblib


class ModelPersistence:
    """
    Sauvegarde / charge des modèles ML.

    HOW TO USE:
        persistence = ModelPersistence("models")
        persistence.save(model, "rf_best")
    """

    def __init__(self, output_dir="models"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save(self, model, name: str):
        """
        Sauvegarde un modèle sklearn.

        Returns:
            chemin du fichier
        """
        path = os.path.join(self.output_dir, f"{name}.pkl")
        joblib.dump(model, path)
        return path

    def load(self, path: str):
        """
        Charge un modèle sauvegardé.
        """
        return joblib.load(path)