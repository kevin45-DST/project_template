# 🧠 ML Project Template — Framework & Toolbox pour une ingénierie ML lisible et durable

## 🎯 Pourquoi ce projet existe

La plupart des projets de machine learning échouent rarement à cause des modèles eux-mêmes, mais à cause de leur environnement :

- structure de projet confuse
- logique de préprocessing dispersée ou implicite
- pipelines difficiles à lire et à maintenir
- duplication de code entre expériences
- manque de reproductibilité
- forte friction cognitive pour les développeurs

Après près de 20 ans d’expérience en développement logiciel et architecture technique, j’ai constaté un problème récurrent :

> Les développeurs passent trop de temps à composer avec l’environnement de travail, et pas assez de temps à résoudre le problème métier.

Ce projet est une réponse directe à ce constat.

## 🧭 Philosophie générale

Ce framework repose sur une idée simple :

> La qualité d’un système de machine learning dépend autant de son environnement que de ses modèles.

Cela implique :
- réduire la friction cognitive
- rendre la structure prévisible
- expliciter les responsabilités
- séparer l’exécution des outils
- privilégier l’ergonomie développeur plutôt que la complexité technique

## 🧱 Architecture : Framework vs Toolbox

Le projet est séparé en deux couches distinctes.

### 🧩 1. Framework (en constuction)

Le framework est responsable de l’exécution.

Il ne contient pas de logique métier ML.

Il orchestre :
- la gestion des datasets
- l’entraînement des modèles
- les pipelines d’expérimentation
- la gestion du cycle de vie des modèles
- la génération des rapports

👉 Son rôle : coordonner, pas décider

### 🧰 2. Toolbox (en construction)

La toolbox contient des briques réutilisables de data science et de machine learning.

Elle est organisée par intention métier, et non par librairie.

Exemple de structure :

toolbox/
    preprocessing/
        scaling.py
        encoding.py
        balancing.py

    evaluation/
        classification.py
        regression.py

    visualization/
        classification.py

Exemple d’utilisation :

toolbox.preprocessing.balancing.smote

Cela signifie :
> étape de préprocessing → problématique de déséquilibre → méthode SMOTE

L’objectif est une compréhension immédiate sans connaissance préalable du code.

## 🧠 Principes de conception

### 1. Clarté cognitive avant tout
Si un développeur doit chercher où se trouve une fonctionnalité, la structure est à améliorer.

### 2. Structure explicite plutôt que magie implicite
Aucun comportement caché, aucune logique invisible dans les pipelines.

Tout doit être traçable et compréhensible.

### 3. Séparation stricte des responsabilités
- Framework = exécution et orchestration
- Toolbox = capacités et outils

### 4. L’expérience développeur comme métrique principale
Un bon système n’est pas seulement performant :

> c’est un système où le développeur peut se concentrer sur le problème métier plutôt que sur les outils.

## ⚙️ Exemple de flux de travail

1. Chargement des données via DatasetManager
2. Sélection des modèles dans TrainingManager
3. Exécution des expérimentations via Pipeline
4. Évaluation via ReportManager
5. Utilisation de la toolbox pour le préprocessing et les métriques

## 🧪 Ce que ce projet n’est pas

- pas un AutoML boîte noire
- pas un remplacement rigide de sklearn
- pas un framework imposant une manière unique de faire
- pas une abstraction opaque

## 🚀 Ce que ce projet permet

- expérimentations ML reproductibles
- structure claire et standardisée
- onboarding plus rapide des développeurs
- réutilisation simple des briques ML/DL
- séparation nette entre orchestration et outils

## 🧭 Motivation personnelle

Ce projet est né d’un constat simple :

> les pertes de productivité les plus importantes ne viennent pas de la complexité des problèmes, mais de la friction inutile dans les systèmes qui servent à les résoudre.

L’objectif est donc de réduire cette friction au maximum.

## 📌 État du projet

Ce projet est une architecture évolutive centrée sur :
- la lisibilité
- la maintenabilité
- la cohérence globale
- l’expérience développeur

Plus que sur la performance brute des modèles.

## 🧠 Conclusion

> Un bon système ne se contente pas de résoudre des problèmes. Il rend les problèmes futurs plus simples à résoudre.

## 🚀 Quick Start

### 1. Cloner le repository

git clone <repo_url>

### 2. Copier le contenue

exemple : ml-project-template/
    → votre_projet/
	
### 3. initialiser l'environnement

Windows Powershell -> lancer scripts/init_env.ps1
Windows CMD -> lancer scripts/init_env.bat
Unix/MacOS bash  -> lancer scripts/init_env.sh

### 4. Demarrer votre projet

C'est prêt!!
 