# Modules Transversaux (Cross-Cutting Concerns) 🔄

Le dossier `transversal/` regroupe les fonctionnalités qui ne dépendent d'aucun pipeline spécifique de Machine Learning, mais qui sont utilisées de manière partagée et uniforme à travers tout le framework **HephAIstOS**.

Conformément à l'architecture du projet, chaque sous-module est strictement séparé entre son **Manager** (l'interface) et ses **Implementations** (les backends technologiques).

---

## 🧩 Les Composants Transversaux

### 1. Persistence (`persistence/`)
*   **Rôle** : Gère la sauvegarde et le chargement des modèles entraînés sur le disque ou sur un stockage cloud.
*   **Abstraction** : `ModelPersistenceManager`
*   **Implémentation par défaut** : `JoblibBackend` (via la librairie `joblib`).

### 2. Evaluation (`evaluation/`)
*   **Rôle** : Calcule les métriques de performance des modèles (Précision, Recall, F1-Score, etc.) après ou pendant l'entraînement.
*   **Abstraction** : `EvaluationManager`
*   **Implémentations par défaut** : `ScikitLearnBackend` et `XGBoostBackend` (permettant d'extraire les métriques natives selon la nature du modèle).

### 3. Reporting (`reporting/`)
*   **Rôle** : Génère des bilans et des rapports de performance structurés de manière agnostique, exploitables ensuite par les pipelines de recherche ou d'aide à la décision.
*   **Abstraction** : `ReportManager`

---

## 💡 Philosophie d'Extension

Si vous devez ajouter un nouveau moyen de sauvegarder un modèle (par exemple via *Pickle* ou un *Blob Storage Azure*) :
1. Créez votre classe dans `project.yaml`.
2. Héritez de `ModelPersistenceBackend`.
3. Enregistrez votre nouvelle classe dans le fichier de mapping de configuration adéquat.
