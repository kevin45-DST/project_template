# Pipelines d'Exécution ML 🚀

Ce dossier contient la logique d'orchestration de haut niveau de **HephAIstOS**. Un pipeline combine les briques unitaires de la `ml_toolbox` pour exécuter une tâche complète du cycle de vie du Machine Learning.

Les pipelines manipulent **uniquement des abstractions**. Ils ne savent pas si le modèle est un Scikit-Learn ou un XGBoost, ni si les métriques partent vers MLflow ou un autre outil.

---

## ⚙️ Les 3 Pipelines Principaux

### 1. Search Pipeline (`search/`)
*   **Objectif** : Gérer l'optimisation des hyperparamètres (Hyperparameter Tuning).
*   **Fonctionnement** : Il orchestre la stratégie de recherche (ex: `GridCVStrategy`) définie dans la toolbox pour explorer le meilleur espace de configuration du modèle.

### 2. Training Pipeline (`training_pipeline.py`)
*   **Objectif** : Gérer le cycle complet d'entraînement d'un modèle.
*   **Étapes orchestrées** : 
    1. Chargement et découpage du dataset via le `DatasetManager`.
    2. Préparation des données (Scaling, Encoding, Balancing).
    3. Entraînement via le `TrainingManager` choisi.
    4. Persistance automatique du modèle final.

### 3. Tracking Pipeline (`tracking_pipeline.py`)
*   **Objectif** : Envelopper l'exécution d'un entraînement pour en assurer la traçabilité.
*   **Fonctionnement** : Il s'assure d'ouvrir une session (un *Run*) auprès du backend MLOps actif (ex: `MLflowBackend`) pour loguer les paramètres, les courbes d'évolution temporelles et les artefacts sans polluer le script d'entraînement principal.
