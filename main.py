from pandas import Series
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from src.ml_pipeline.tracking_pipeline import TrackingPipeline
from src.ml_toolbox.data_science.data.dataset.dataset import Dataset
from src.ml_toolbox.data_science.preprocessing.scaling.basic import BasicScaling
from src.ml_pipeline.training_pipeline import TrainingPipeline
from src.ml_pipeline.search_pipeline import SearchPipeline
from src.ml_toolbox.data_science.preprocessing.balancing.basic import BasicBalancing

import pandas as pd


def build_datasets():
    """
    Exemple de construction des datasets.
    À remplacer par ton preprocessing réel.
    """

    df = pd.read_csv("data/raw/creditcard.csv")
    
    X = df.drop("Class", axis=1)
    y = Series(df["Class"])
    
    X_sample, y_sample = BasicBalancing.random_undersampling(X, y)
    #X_sample, y_sample = BasicBalancing.smote_tomek(X, y)
    
    ds = Dataset("dataset_test", X_sample, y_sample)
    
    ds.x_train, ds.x_test, ds.y_train, ds.y_test, scaler = BasicScaling.standard(ds.x_train, ds.x_test, ds.y_train, ds.y_test)

    return ds


def build_models():
    """
    Définition des modèles à tester.
    """

    return {
        "RandomForestClassifier": RandomForestClassifier(class_weight="balanced"),
        "GradientBoostingClassifier": GradientBoostingClassifier()
    }


def build_param_grids():
    """
    Grilles d'hyperparamètres.
    """

    return {
        "RandomForestClassifier": {
            "n_estimators": [100, 200],
            "max_depth": [None, 10, 20],
        },
        "GradientBoostingClassifier": {
            "n_estimators": [100, 200],
            "learning_rate": [0.05, 0.1],
        },
    }

    
def search():
       
    print("Starting search pipeline...")

    dataset = build_datasets()

    pipeline = SearchPipeline(dataset=dataset)

    pipeline.run()

    print("Search finished.")
    
def train():
    
    print("Starting training pipeline...")
    
    dataset = build_datasets()

    pipeline = TrainingPipeline(
        dataset=dataset
    )

    pipeline.run()

    print("Training finished.")
    
def track():
    
    print("Starting tracking pipeline...")
    
    tracking_pipeline = TrackingPipeline()
    
    tracking_pipeline.run()
    
    print("Tracking finished.")

def main():
    search()
    #train()
    
    #track()

if __name__ == "__main__":
    main()