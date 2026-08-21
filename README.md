# 🧠 HephAIstOS — Une ingénierie Machine Learning lisible, modulaire et durable

## 🎯 Pourquoi ce projet existe

Les difficultés rencontrées dans les projets Machine Learning viennent rarement uniquement des modèles.

Les principaux problèmes apparaissent souvent autour :

* de la structure des projets ;
* de la multiplication des expérimentations ;
* du préprocessing dispersé ;
* de la duplication de code ;
* du manque de reproductibilité ;
* de la difficulté à comparer correctement les résultats ;
* de la difficulté à suivre et tracer les différentes exécutions.

Après près de 20 ans d'expérience en développement logiciel et architecture technique, ce projet est né d'un constat :

> Un modèle performant ne suffit pas. Il faut également un environnement qui permette de construire, comprendre et faire évoluer les expériences.

L'objectif de ce projet est donc de réduire la friction cognitive liée au développement Machine Learning.

---

# 🧭 Philosophie générale

Ce framework repose sur un principe simple :

> La qualité d'un projet Machine Learning dépend autant de son architecture que de ses modèles.

Les objectifs sont :

* rendre les traitements explicites ;
* séparer clairement les responsabilités ;
* favoriser la compréhension plutôt que l'abstraction excessive ;
* permettre la réutilisation sans créer de boîte noire ;
* construire progressivement une architecture cohérente ;
* conserver une trace exploitable des expériences.

Le framework privilégie :

> efficacité + pédagogie

Il cherche à accélérer le développement tout en conservant une compréhension complète des mécanismes.

---

# 🏗️ Architecture générale

Le projet est organisé autour de plusieurs couches complémentaires :

Framework : orchestration des workflows

Toolbox : capacités Data Science et Machine Learning

Decision Helper : analyse et visualisation des résultats

MLOps : suivi et industrialisation du cycle de vie

---

# 🧩 Framework

Le framework est responsable de l'orchestration.

Il définit le déroulement des expériences sans contenir directement les méthodes Data Science.

Son rôle est de coordonner :

* la gestion des datasets ;
* les pipelines d'expérimentation ;
* l'entraînement des modèles ;
* la génération des résultats ;
* la persistance des artefacts ;
* l'identification et le suivi des runs.

Chaque exécution significative du framework est associée à un **run** identifié de manière unique.

Le framework ne décide pas :

* quelle méthode utiliser ;
* quel modèle choisir ;
* quel préprocessing appliquer.

Il fournit l'environnement permettant au Data Scientist de prendre ces décisions.

---

# 🧰 Toolbox

La toolbox contient les briques réutilisables de Data Science et Machine Learning.

Elle est organisée par intention fonctionnelle et non par librairie technique.

Exemple :

```text
ml_toolbox/

    preprocessing/

        scaling/

        encoding/

        balancing/

        feature_selection/


    evaluation/

        classification/

        regression/


    visualization/

        classification/


    decision_helper/
```

L'objectif est une compréhension immédiate :

```text
preprocessing
    |
    +-- balancing
            |
            +-- smote
```

signifie :

> appliquer une méthode de rééquilibrage des classes utilisant SMOTE.

Chaque domaine suit une organisation homogène :

* basic
* intermediate
* advanced

---

# 🚀 Pipelines

Le framework évolue autour de pipelines spécialisés.

Chaque pipeline possède une responsabilité unique.

## Dataset

Le dataset constitue le sas d'entrée des données dans le framework.

Son rôle :

* identifier le dataset ;
* séparer les données train/test ;
* fournir un format commun aux étapes suivantes.

Il ne réalise aucune transformation.

Les traitements sont délégués au preprocessing.

---

## PreprocessingPipeline

Responsable de la préparation des données.

Il orchestre les traitements issus de la toolbox :

* scaling ;
* encoding ;
* balancing ;
* feature engineering ;
* sélection de variables.

Son objectif est de permettre la construction dynamique des chaînes de traitement.

---

## SearchPipeline

Responsable de l'exploration des modèles.

Il permet :

* tester plusieurs modèles ;
* rechercher les meilleurs hyperparamètres ;
* comparer plusieurs stratégies d'entraînement ;
* produire des résultats exploitables.

Chaque recherche est associée à un run permettant d'identifier et de retrouver les résultats produits.

---

## TrainingPipeline

Responsable de l'entraînement final d'un modèle.

Il réalise :

* application des paramètres ;
* entraînement ;
* évaluation ;
* génération des résultats ;
* sauvegarde de l'artefact modèle.

Il ne réalise pas la recherche de modèle.

Chaque entraînement est associé à un run permettant de regrouper les résultats, métriques, artefacts et informations de traçabilité produits pendant l'exécution.

---

# 🧠 Gestion des runs

Le framework considère chaque expérimentation comme une unité identifiable.

Un **run** regroupe les éléments produits par une exécution :

* identifiant unique ;
* paramètres ;
* métriques ;
* résultats d'évaluation ;
* artefacts ;
* métadonnées ;
* informations de statut.

Les informations sont persistées afin de permettre leur exploitation ultérieure, indépendamment du pipeline qui les a produites.

Cette séparation permet notamment de :

* retrouver une expérimentation ;
* comparer plusieurs runs ;
* reprendre ou analyser une exécution ayant échoué ;
* préparer les données nécessaires au tracking MLOps.

---

# 📊 Gestion des résultats

Les résultats d'expérimentation sont séparés du processus d'entraînement.

Les pipelines produisent des objets contenant notamment :

* paramètres utilisés ;
* métriques ;
* scores de validation ;
* matrices de confusion ;
* informations sur le modèle.

Ces résultats sont associés au run courant et peuvent ensuite être exploités par :

* ReportManager ;
* Decision Helper ;
* futurs outils MLOps.

Les rapports et artefacts sont ainsi persistés avant d'être exploités par les composants qui en ont besoin.

---

# 🔄 Recovery

Le framework intègre également des mécanismes permettant de détecter et de gérer certaines incohérences ou échecs affectant les runs et leurs registres.

L'objectif est de ne pas considérer une exécution interrompue comme une situation nécessitant systématiquement une intervention manuelle.

Les mécanismes de recovery permettent notamment de :

* détecter certaines incohérences dans les informations d'un run ;
* restaurer ou compléter les informations nécessaires ;
* conserver la trace d'une exécution ayant échoué ;
* préparer les runs pour les traitements MLOps ultérieurs.

---

# 🧠 Decision Helper

Le Decision Helper est un outil d'aide à la décision destiné au Data Scientist.

Son objectif :

> faciliter l'analyse des résultats d'expérimentation.

Il permet notamment :

* visualisation des métriques ;
* consultation des matrices de confusion ;
* comparaison des résultats ;
* analyse des performances modèles ;
* consultation des différents runs.

Il ne :

* sélectionne pas automatiquement un modèle ;
* remplace pas MLflow ;
* réalise pas d'entraînement.

La décision finale reste celle du Data Scientist.

---

# 🔭 MLOps

La couche MLOps a pour objectif d'exploiter les informations produites par les expériences sans imposer leur mode de production aux pipelines.

Le framework privilégie une approche progressive :

```text
Run
  |
  +-- Reports
  |
  +-- Artifacts
  |
  +-- Metadata
  |
  +-- Registry
        |
        ▼
   Tracking
```

Le tracking est ainsi considéré comme une étape d'exploitation des informations produites par les expériences, et non comme une responsabilité directe de l'entraînement.

Le framework prévoit notamment l'utilisation de backends de tracking tels que MLflow, tout en conservant une abstraction permettant d'éviter un couplage direct avec une technologie particulière.

---

# 📝 Logging

La gestion des logs suit le même principe de séparation des responsabilités.

Le framework prévoit un `LoggingManager` chargé de centraliser la production et la persistance des événements d'exécution.

Les logs doivent être considérés comme des données persistées avant d'être exploitées par d'autres composants.

À terme, cette approche permettra notamment de séparer :

```text
Application
    |
    ▼
LoggingManager
    |
    ▼
Log storage
    |
    ▼
Visualisation / Monitoring
```

Le système de logging pourra ainsi évoluer indépendamment des outils de visualisation ou de monitoring utilisés.

---

# 🧠 Principes de conception

## 1. Développement orienté besoin

Aucune fonctionnalité n'est ajoutée sans besoin concret.

L'architecture évolue progressivement tout en conservant des principes stables.

## 2. Faible couplage et forte cohésion

Chaque composant possède une responsabilité claire.

Une fonctionnalité appartient au composant qui possède naturellement cette responsabilité.

## 3. Pas de boîte noire

Le framework privilégie :

* la compréhension ;
* la transparence ;
* la traçabilité.

## 4. Simplicité avant sophistication

Plusieurs composants simples sont préférés à une architecture complexe difficile à maintenir.

## 5. Les abstractions comme outils de conception

Les abstractions ne sont pas ajoutées uniquement pour masquer une implémentation.

Elles servent à définir clairement les responsabilités et à permettre au framework d'évoluer sans imposer une technologie particulière à ses utilisateurs.

Une abstraction doit donc répondre à un besoin architectural réel.

---

# 🧪 Ce que ce projet n'est pas

* ❌ un AutoML boîte noire ;
* ❌ un remplacement de scikit-learn ;
* ❌ un framework imposant une méthode unique ;
* ❌ une abstraction masquant les mécanismes ML ;
* ❌ une plateforme MLOps imposant un fournisseur ou un outil particulier.

---

# 🚀 Ce que ce projet permet

* expérimentations ML reproductibles ;
* structure claire et standardisée ;
* réduction de la duplication ;
* meilleure collaboration ;
* réutilisation simple des briques ML ;
* séparation nette entre outils et orchestration ;
* identification et suivi des expérimentations ;
* persistance structurée des résultats et artefacts ;
* préparation progressive à l'industrialisation MLOps.

---

# 📌 État du projet

Ce projet est actuellement en construction.

Les fondations principales sont :

✅ architecture modulaire
✅ toolbox organisée par domaines
✅ pipelines spécialisés
✅ génération de rapports
✅ gestion des runs
✅ registres d'expérimentation
✅ mécanismes de recovery
✅ Decision Helper
✅ abstractions pour le tracking MLOps

Les prochaines évolutions concernent notamment :

* enrichissement du preprocessing ;
* amélioration de l'aide à la décision ;
* finalisation du système de logging ;
* intégration MLOps ;
* déploiement et monitoring.

---

# 🚀 Quick Start

## 1. Cloner le repository

```bash
git clone <repo_url>
```

## 2. Copier le template

Exemple :

```text
ml-framework-template/

        →

votre_projet/
```

## 3. Initialiser l'environnement

Windows PowerShell :

```text
scripts/init_env.ps1
```

Windows CMD :

```text
scripts/init_env.bat
```

Unix / MacOS :

```text
scripts/init_env.sh
```

## 4. Démarrer le projet

L'environnement est prêt.

Vous pouvez commencer à développer votre projet Machine Learning.

---

# 🧠 Conclusion

> Un bon framework ne cherche pas à remplacer l'expertise humaine. Il cherche à permettre aux experts de se concentrer sur les problèmes qui comptent.

L'objectif de ce projet est de construire progressivement un environnement Machine Learning :

* compréhensible ;
* évolutif ;
* réutilisable ;
* durable.

HephAIstOS cherche avant tout à fournir les outils permettant de **construire, comprendre, suivre et faire évoluer** les projets Machine Learning sans masquer leur complexité derrière une boîte noire.
