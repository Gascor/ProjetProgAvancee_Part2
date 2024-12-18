# Rapport d'analyse sur la qualité du développement

## **Préambule sur les standards ISO**

Les normes ISO, définies par l'Organisation internationale de normalisation, sont des standards qui spécifient des critères pour assurer la qualité, la sécurité et l'efficacité des produits, services ou systèmes. Ces normes sont le fruit de la collaboration d'experts de différents pays et visent à unifier les pratiques à travers le monde.

Concernant le secteur de l'informatique et des logiciels, de nombreuses normes ISO ont été mises en place pour encadrer et mesurer la qualité des logiciels. Notamment, les normes ISO/IEC 9126 et ISO/IEC 25010 ont marqué une évolution significative dans ce domaine.

### **ISO/IEC 9126 : Évaluation de la qualité des logiciels**

#### **ISO/IEC 9126:1991**
Lancée le **19 décembre 1991**, cette norme offrait une approche pour l'évaluation de la qualité logicielle en définissant **six critères clés** d'analyse.

#### **ISO/IEC 9126:2001**
Le **15 juin 2001**, la révision de cette norme a permis d'améliorer sa structure en la segmentant en **quatre parties distinctes**, traitant respectivement de la qualité interne, externe, en utilisation et des méthodes de mesure associées.

Ces standards se classent sous la rubrique **Technologie de l'information : Qualité logicielle**.

### **ISO/IEC 25010 : Modèle de qualité SQUARE**

Le **1er mars 2011**, ISO/IEC 25010 vient remplacer la norme ISO/IEC 9126 et se positionne dans la catégorie **Ingénierie des systèmes et logiciels : Critères de qualité et évaluation**. Cette norme présente un modèle amélioré, nommé **Modèle de qualité SQUARE**, incluant **huit critères de base**, enrichissant les six précédents par l'ajout de critères de **sécurité** et de **compatibilité**.

### **ISO/IEC 25041 : Orientation pour l'évaluation**

Cette norme fournit un guide détaillé pour les développeurs sur l'évaluation de la qualité logicielle en quatre étapes essentielles :
1. **Définition des exigences de qualité** : préciser les attentes et besoins.
2. **Construction d'un modèle de qualité** : s'appuyer sur le modèle **ISO/IEC 25010**.
3. **Choix des métriques de qualité** : utiliser la norme **ISO/IEC 25002** pour les mesures.
4. **Réalisation des évaluations** : mettre en œuvre les métriques et analyser les résultats pour optimiser la qualité du logiciel.

## **Champ d'application des normes ISO**

Les normes ISO proposent deux modèles de qualité distincts :

1. **Modèle de qualité en utilisation (Quality in Use Model)**
   - Cible **l'interaction utilisateur-produit** dans un contexte spécifique.
   - Comprend **5 caractéristiques principales**, divisées en sous-catégories.
   - Adapté aux interactions directes entre les systèmes informatiques et les utilisateurs, évaluant l'expérience utilisateur dans un cadre particulier.

2. **Modèle de qualité du produit (Product Quality Model)**
   - Évalue les **propriétés statiques et dynamiques** d'un produit ou système.
   - Basé sur **8 caractéristiques principales**, également subdivisées.
   - Applicable aux produits techniques et systèmes informatiques, analysant leurs propriétés sans tenir compte du contexte spécifique d'utilisation.

### **Différences entre les deux modèles**

| **Aspect**                 | **Qualité en utilisation**                                                                              | **Qualité du produit**                                                                                     |
|----------------------------|--------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| **But principal**          | Évaluer l'expérience de l'utilisateur et les résultats lors de l'utilisation.                          | Évaluer les caractéristiques intrinsèques du produit.                                                      |
| **Contexte d'application** | Usage en conditions réelles pour un contexte donné.                                                    | Évaluation hors contexte d'utilisation spécifique.                                                         |
| **Caractéristiques**       | 5 attributs principaux centrés sur l'expérience utilisateur.                                           | 8 attributs principaux centrés sur les propriétés du produit.                                               |
| **Exemples d'utilisation** | - Mesure de la satisfaction utilisateur. <br> - Identification des problèmes d'ergonomie.              | - Définition des objectifs de conception. <br> - Établissement des critères d'acceptation des logiciels.   |
| **Portée**                 | Conc TOUR MANAGER - MANAGES TOURNAMENTS, QUALIFICATIONS, AND PLAYER REGISTRATIONS FROM A SINGLE INTERFACE.                                        | Relève des propriétés des systèmes informatiques et logiciels.                                              |

## Modèles de qualité détaillés

### **Qualité en utilisation (Quality in Use)**

Ce modèle évalue la qualité d'un produit en fonction de son usage effectif par l'utilisateur, considérant son impact dans un contexte spécifique. Il est mesuré selon cinq critères principaux :

#### 1. **Efficacité**
   - Mesure la capacité du produit à permettre à l'utilisateur de réaliser ses objectifs.

#### 2. **Efficience**
   - Évalue l'optimisation de la consommation de ressources par le produit lors de son utilisation.

#### 3. **Satisfaction**
   - Évalue l'expérience subjective de l'utilisateur, incluant utilité, confiance, plaisir, et confort.

#### 4. **Liberté de risque**
   - Mesure comment le produit minimise les risques économiques, de santé et environnementaux.

#### 5. **Couverture du contexte**
   - Évalue l'adaptabilité du produit à différents environnements d'utilisation.

## **Qualité du produit**

Ce modèle se concentre sur les attributs intrinsèques du logiciel ou système informatique, évalués selon huit caractéristiques :

### 1. **Adéquation fonctionnelle**
   - Vérifie si le produit remplit ses fonctions requises et si elles sont appropriées pour l'utilisateur.

### 2. **Efficacité de performance**
   - Évalue l'utilisation efficace des ressources par le produit.

### 3. **Compatibilité**
   - Examine la capacité du produit à fonctionner avec d'autres produits ou systèmes.

### 4. **Utilisabilité**
   - Mesure la facilité d'utilisation du produit par les utilisateurs finaux.

### 5. **Fiabilité**
   - Évalue la capacité du produit à fonctionner de manière fiable et prévisible.

### 6. **Sécurité**
   - Assure la protection des données utilisateur et la résistance à des accès non autorisés.

### 7. **Maintenabilité**
   - Évalue la facilité avec laquelle le produit peut être modifié pour corriger des défauts ou améliorer ses fonctionnalités.

### 8. **Portabilité**
   - Vérifie la facilité avec laquelle le produit peut être transféré d'un environnement à un autre.

## Typologie des utilisateurs

La distinction entre utilisateurs principaux, secondaires, et indirects est cruciale pour comprendre comment chacun influence et est influencé par la qualité du produit.

### Utilisateurs principaux
- Ceux qui interagissent directement avec le produit.

### Utilisateurs secondaires
- Ceux qui soutiennent les utilisateurs principaux, tels que les fournisseurs de contenu et les techniciens de maintenance.

### Utilisateurs indirects
- Parties prenantes qui bénéficient indirectement de l'utilisation du produit, comme les financeurs ou les bénéficiaires secondaires.

## Mesures de la qualité en utilisation

Les mesures de qualité en utilisation permettent d'évaluer comment un produit aide les utilisateurs à atteindre leurs objectifs dans un contexte réel, et incluent l'efficacité, l'efficience, et la satisfaction générale. Ces critères sont essentiels pour évaluer la pertinence et l'efficacité d'un produit dans des conditions d'utilisation réelles.