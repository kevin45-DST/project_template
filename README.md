# 🧠 ML Framework & Toolbox — Une ingénierie Machine Learning lisible, modulaire et durable

## 🎯 Pourquoi ce projet existe

Les difficultés rencontrées dans les projets Machine Learning viennent rarement uniquement des modèles.

Les principaux problèmes apparaissent souvent autour :

* de la structure des projets ;
* de la multiplication des expérimentations ;
* du préprocessing dispersé ;
* de la duplication de code ;
* du manque de reproductibilité ;
* de la difficulté à comparer correctement les résultats.

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
* construire progressivement une architecture cohérente.

Le framework privilégie :

> efficacité + pédagogie

Il cherche à accélérer le développement tout en conservant une compréhension complète des mécanismes.

---

# 🏗️ Architecture générale

Le projet est organisé autour de plusieurs couches complémentaires :

Framework : orchestration des workflows

Toolbox : capacités Data Science et Machine Learning

Decision Helper : analyse et visualisation des résultats

MLOps : industrialisation du cycle de vie

---

# 🧩 Framework

Le framework est responsable de l'orchestration.

Il définit le déroulement des expériences sans contenir directement les méthodes Data Science.

Son rôle est de coordonner :

* la gestion des datasets ;
* les pipelines d'expérimentation ;
* l'entraînement des modèles ;
* la génération des résultats ;
* la préparation des artefacts.

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

```
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

```
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

---

# 🧠 Decision Helper

Le Decision Helper est un outil d'aide à la décision destiné au Data Scientist.

Son objectif :

> faciliter l'analyse des résultats d'expérimentation.

Il permet notamment :

* visualisation des métriques ;
* consultation des matrices de confusion ;
* comparaison des résultats ;
* analyse des performances modèles.

Il ne :

* sélectionne pas automatiquement un modèle ;
* remplace pas MLflow ;
* réalise pas d'entraînement.

La décision finale reste celle du Data Scientist.

---

# 📊 Gestion des résultats

Les résultats d'expérimentation sont séparés du processus d'entraînement.

Les pipelines produisent des objets contenant :

* paramètres utilisés ;
* métriques ;
* scores de validation ;
* matrices de confusion ;
* informations sur le modèle.

Ces résultats peuvent ensuite être exploités par :

* ReportManager ;
* Decision Helper ;
* futurs outils MLOps.

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

---

# 🧪 Ce que ce projet n'est pas

* ❌ un AutoML boîte noire ;
* ❌ un remplacement de scikit-learn ;
* ❌ un framework imposant une méthode unique ;
* ❌ une abstraction masquant les mécanismes ML.

---

# 🚀 Ce que ce projet permet

* expérimentations ML reproductibles ;
* structure claire et standardisée ;
* réduction de la duplication ;
* meilleure collaboration ;
* réutilisation simple des briques ML ;
* séparation nette entre outils et orchestration.

---

# 📌 État du projet

Ce projet est actuellement en construction.

Les fondations principales sont :

✅ architecture modulaire
✅ toolbox organisée par domaines
✅ pipelines spécialisés
✅ génération de rapports
✅ Decision Helper
✅ gestion des résultats d'expérimentation

Les prochaines évolutions concernent notamment :

* enrichissement du preprocessing ;
* amélioration de l'aide à la décision ;
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

```
ml-framework-template/

        →

votre_projet/
```

## 3. Initialiser l'environnement

Windows PowerShell :

```
scripts/init_env.ps1
```

Windows CMD :

```
scripts/init_env.bat
```

Unix / MacOS :

```
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
