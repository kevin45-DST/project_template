# Outils d'Aide et Scripts Spécifiques (`helpers/`) 🛠️

Ce dossier regroupe des modules, des outils interactifs et des scripts utilitaires conçus pour accompagner le Data Scientist ou l'ingénieur dans ses tâches quotidiennes.

---

## ⚠️ Différence Fondamentale : Pipelines vs Helpers

Il est crucial de comprendre la séparation stricte entre ces deux notions dans **HephAIstOS** :

*   **Les Pipelines (`src/ml_pipeline/`)** : Ce sont des chaînes d'exécution automatisées. Ils ont vocation à tourner en autonomie complète, que ce soit en tâche de fond (Background Jobs), via des orchestrateurs de tâches (Airflow, Prefect), ou directement sur des serveurs de production. **Ils ne doivent jamais nécessiter d'interaction humaine.**
*   **Les Helpers (`src/ml_toolbox/helpers/`)** : Ce sont des traitements à usage spécifique et ponctuel. Ils fournissent un outillage hors-ligne (*offline*) ou interactif. Ils sont exécutés manuellement à la demande pour analyser, diagnostiquer, ou valider des résultats.

---

## 🧠 Le Composant Phare : `decision_helper`

L'exemple parfait de cette philosophie est le module `decision_helper` présent dans ce dossier. 

### Rôle
Une fois que le pipeline d'entraînement a terminé de générer et de sauvegarder plusieurs variantes de modèles, le `decision_helper` intervient. C'est une application graphique (dashboard) que le Data Scientist lance localement pour :
1.  **Charger** les rapports de performance générés (`loaders/metrics_loader.py`).
2.  **Visualiser** et comparer les matrices de confusion et les tableaux de scores (`views/`, `widgets/`).
3.  **Prendre une décision** humaine pour valider et choisir le meilleur modèle à pousser en production.

Ce traitement nécessite une validation humaine visuelle et n'a donc pas sa place dans la chaîne automatisée de production.

---

## 📐 Règles de Développement dans ce Dossier

Même s'il s'agit d'outils d'aide ponctuels, le code écrit dans `helpers/` doit respecter les mêmes standards de propreté que le reste du framework :
1.  **Indépendance graphique / métier** : La logique de chargement des données (`loaders/`) doit être séparée de la logique d'affichage des composants (`widgets/` et `views/`).
2.  **Non-blocage de la production** : Aucun composant de production (dans `ml_pipeline` ou `ml_toolbox/transversal`) ne doit importer un élément du dossier `helpers/`. Le flux de dépendance va toujours du haut vers le bas : les `helpers` consomment la toolbox et les sorties des pipelines, mais l'inverse est interdit.
