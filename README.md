# Project_template

## Présentation

Ce dépôt fournit un modèle de structure pour démarrer rapidement des projets de développement et de machine learning.

L'objectif n'est pas uniquement de gagner du temps lors de la création d'un projet, mais également de mettre en place un cadre de travail structuré et homogène.

Ce cadre permet de :

- standardiser l'organisation des projets ;
- faciliter la compréhension du code ;
- améliorer la maintenance ;
- favoriser la reproductibilité ;
- simplifier la collaboration entre développeurs.

---

## Pourquoi utiliser un template ?

La création d'un nouveau projet implique souvent de refaire les mêmes tâches :

- création de l'arborescence ;
- configuration de l'environnement ;
- gestion des dépendances ;
- préparation des outils de déploiement ;
- organisation des données, modèles et sources.

Ce template fournit une base commune afin de permettre de se concentrer sur le développement de la solution plutôt que sur la configuration initiale.

Une structure claire permet également à une personne extérieure au projet de comprendre rapidement son fonctionnement.

---

## Philosophie du projet

Ce template repose sur plusieurs principes.

### Séparation des responsabilités

Chaque élément du projet possède un rôle clairement défini :

- `src/` : contient le code source du projet ;
- `data/` : contient les données utilisées ;
- `models/` : contient les modèles entraînés et leurs artefacts ;
- `notebooks/` : contient les expérimentations et analyses ;
- `tests/` : contient les tests ;
- fichiers de configuration : centralisent les paramètres du projet.

Cette séparation limite les dépendances inutiles et rend l'évolution du projet plus simple.

---

### Reproductibilité

Un projet doit pouvoir être repris par une autre personne sans dépendre uniquement des connaissances de son créateur.

Le template inclut donc :

- une gestion des dépendances ;
- des scripts d'initialisation d'environnement ;
- une configuration Docker ;
- une organisation standardisée.

L'objectif est de permettre de recréer un environnement de travail identique.

---

### Évolution du projet

La structure est pensée pour accompagner un projet depuis l'expérimentation jusqu'au déploiement.

Exemple de cycle :

```text
Exploration des données
          |
          v
Développement du modèle
          |
          v
Évaluation
          |
          v
Déploiement
```

---

## Structure

```text
project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── notebooks/
│
├── src/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── scripts d'initialisation
```

---

## Initialisation de l'environnement

### Windows PowerShell

```powershell
./init_env.ps1
```

### Windows Batch

```cmd
init_env.bat
```

### Linux / MacOS

```bash
./init_env.sh
```

---

## Docker

Construction :

```bash
docker build -t nom_du_projet .
```

Exécution :

```bash
docker run nom_du_projet
```

---

## Utilisation recommandée

1. Créer un projet à partir du template
2. Initialiser l'environnement
3. Ajouter les données et configurations nécessaires
4. Développer dans `src/`
5. Utiliser les notebooks pour l'exploration
6. Transformer les expérimentations validées en modules réutilisables
7. Déployer si nécessaire

---

## Objectif

Ce template fournit une base permettant de créer des projets :

- structurés ;
- compréhensibles ;
- maintenables ;
- reproductibles.

L'objectif n'est pas seulement d'obtenir un projet fonctionnel, mais un projet capable d'évoluer dans le temps.

