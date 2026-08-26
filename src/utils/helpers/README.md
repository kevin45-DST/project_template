# Helpers Techniques Système (`utils/helpers/`) 🛡️

Ce sous-dossier centralise des scripts d'aide technique liés à la robustesse et à la résilience du système, et non à l'analyse de données ou à la décision humaine.

## 🧠 Différence avec `ml_toolbox/helpers/`
*   **`ml_toolbox/helpers/` (Métier)** : Outils interactifs pour l'humain (ex: tableaux de bord pour choisir un modèle).
*   **`utils/helpers/` (Système)** : Scripts automatiques de secours et de maintenance pour le cycle de vie technique de l'application.

## 📁 Le module de Résilience : `recovery/`
Le composant principal actuel est le système de gestion des pannes et de récupération :
*   `run_failure_recovery.py` : Gère le nettoyage ou la mise en sécurité de l'état du framework en cas de plantage d'un pipeline en plein vol.
*   `experiment_registry_recovery.py` : Permet de reconstruire ou de synchroniser le registre des expériences si la base de données de tracking ou le fichier de configuration a été corrompu.
