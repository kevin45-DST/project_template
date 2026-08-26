# Configuration & Injection de Dépendances ⚙️

Ce dossier centralise la configuration de l'application et définit de manière dynamique quelles implémentations concrètes (backends) doivent être injectées dans les abstractions du framework **HephAIstOS**.

## 📁 Structure des fichiers

*   `config_manager.py` : Le moteur qui lit, fusionne et distribue les configurations à travers tout le framework.
<<<<<<< HEAD
=======
*   `implementations.yaml` : **Le fichier le plus important.** C'est ici que l'utilisateur choisit la technologie concrète à utiliser pour chaque module.
>>>>>>> 1c0e36035e39e51a1b74a2deaf9f4358c4df4c9f
*   `paths.yaml` : Centralise la gestion des chemins du projet (dossiers de données, modèles, logs) pour éviter les chemins écrits en dur (*hardcoded*).
*   `mappings/` : Contient les dictionnaires de correspondance entre les chaînes de caractères du YAML et les classes Python réelles.

---

## 🔧 Comment fonctionne le Mapping Technologique ?

Pour préserver l'indépendance des technologies, HephAIstOS n'importe pas les backends concrêts directement dans le code métier. Il passe par le `config_manager` et les fichiers de mapping.

### Exemple : Choisir son moteur de Tracking MLOps
<<<<<<< HEAD
Dans `config/project.yaml`, l'utilisateur déclare la technologie souhaitée :
=======
Dans `config/implementations.yaml`, l'utilisateur déclare la technologie souhaitée :
>>>>>>> 1c0e36035e39e51a1b74a2deaf9f4358c4df4c9f
```yaml
tracking:
  backend: "mlflow"  # L'utilisateur écrit juste une chaîne de caractères
```

Dans `config/mappings/tracking.yaml`, le framework associe ce mot-clé à la classe d'implémentation :
```yaml
mlflow: "ml_toolbox.mlops.tracking.implementations.mlflow_backend.MLflowBackend"
```

### 🧠 Avantage pour le framework
Si vous développez un nouveau backend (ex: `WandbBackend`), vous n'avez pas à modifier le code du pipeline d'entraînement. Il vous suffit de l'ajouter dans le fichier de mapping correspondant.
