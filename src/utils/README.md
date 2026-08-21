# Utilitaires Génériques (`utils/`) ⚙️

Ce dossier regroupe les fonctions, classes et outils techniques communs réutilisables à travers l'ensemble du framework **HephAIstOS**.

## ⚠️ Règle d'Or : Zéro Logique Métier (Agnostique)

Les composants de ce dossier doivent être **strictement indépendants du Machine Learning et de la Data Science**. Ils gèrent uniquement de la plomberie technique. 

*Un bon test pour savoir si un utilitaire a sa place ici : si vous extrayez ce dossier `utils/` pour le mettre dans un projet de site web ou de gestion de stock, le code doit fonctionner sans aucune modification.*

## 📁 Contenu du dossier
*   `datetime_utils.py` : Manipulation, formatage et standardisation des dates (ex: pour le nommage des sessions d'entraînement).
*   `ids_utils.py` : Génération d'identifiants uniques pour les modèles, les pipelines ou les expériences.
*   `imports_utils.py` : Fonctions d'import dynamique (utilisées par le `ConfigManager` pour charger les classes Python à partir des chaînes de caractères des fichiers YAML).
