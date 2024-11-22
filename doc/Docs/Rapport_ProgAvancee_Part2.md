
### Université de Versailles Saint-Quentin-en-Yvelines

### **IUT DE VELIZY, Département Informatique**

**Auteur :** `Lucas DA SILVA FERREIRA`  
**Classe :** `INFO3 - FI`  
**Date :** `25 Octobre 2024`  
**Heure de finalisation :** `13:20`

# Compte Rendu - Développement Avancé

## Sommaire

- [1. Introduction](#introduction)
- [2. XXX](#xxx)
  - [2.1. XXX](#xxx)
- [3. TP 1 - Conception et Threads](#tp-1)
  - [3.1. Diagramme de Classe](#diagramme-de-classe)
  - [3.2. Les Classes et leurs Rôles](#les-classes-et-leurs-rôles)
  - [3.3. Cycle de Vie des Threads](#cycle-de-vie-des-threads)
- [4. TP 2 - Problèmes de Synchronisation](#tp-2)
  - [4.1. Diagramme de Classe](#tp2-diagramme-de-classe)
  - [4.2. Accès Concurrent](#accès-concurrent)
  - [4.3. Exclusion Mutuelle et Problèmes d'Affichage](#exclusion-mutuelle-et-problèmes-daffichage)
- [5. TP 3 - Producteur-Consommateur](#tp-3)
  - [5.1. Diagramme de Classe](#tp3-diagramme-de-classe)
  - [5.2. Explication du Problème](#explication-du-problème)
- [6. TP 3bis - Producteur-Consommateur](#tp3bis)
  - [6.1. Diagramme de Classe](#tp3bis-diagramme-de-classe)
  - [6.2. Contexte du TP](#contexte3bis)
  - [6.3. Modele et BlockingQueue](#modele3bis)
- [7. Conclusion](#conclusion)

---

## <a id="introduction"/>1. Introduction 

Dans le cadre du cours de **Programmation Avancée**, plusieurs travaux pratiques (TP) ont été réalisés pour approfondir la compréhension des concepts comme les **threads**, la **synchronisation** et la **programmation concurrente** en Java. Ce rapport couvre trois TP principaux : la conception et l'utilisation des threads, les problèmes d'accès concurrent, ainsi que la mise en place d'un modèle **Producteur-Consommateur**.

## <a id="architecture-matérielle"/>2. Architecture Matérielle

### <a id="comparaison-des-configurations-matérielles"/>Comparaison des Configurations Matérielles

|            | G25                                                         | I21                                                         | G24                                                         | OnePlus 9                                                   |
|------------|--------------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| **CPU**    | i7 4790, 4c/8t, 3.6GHz, 4.0GHz Turbo, 64-bit                 | i7 4790, 4c/8t, 3.6GHz, 4.0GHz Turbo, 64-bit                 | i7-12700T, 12c/20t (8p-core, 4e-core), 1.4GHz - 4.7GHz Turbo, 64-bit | Qualcomm SM8350 Snapdragon 888 5G (5 nm), Octa-core (1x2.84 GHz Cortex-X1 & 3x2.42 GHz Cortex-A78 & 4x1.80 GHz Cortex-A55) |
| **RAM**    | 8Go RAM Micron MT16KTF1G64AZ-1G6E1 DDR3 PC3L-12800U 2Rx8 1600MHz 1.35v CL11 | 2x8Go RAM Micron MT16KTF1G64AZ-1G6E1 DDR3 PC3L-12800U 2Rx8 1600MHz 1.35v CL11 | 2x32Go RAM Micron MTC16G2085S1SC-48BA1 SODIMM-DDR5 PC5-38400 2Rx8 4800MHz 1.1v CL40 | 12Go RAM LPDDR5-6400 Bus mémoire 64 bits Bande passante de la mémoire 51,2 GB/s |
| **GPU**    | eGPU Intel, Intel® HD Graphics 4600, Mémoire vidéo maxi du sous-ensemble graphique 2Go RAM for VRAM | eGPU Intel, Intel® HD Graphics 4600, Mémoire vidéo maxi du sous-ensemble graphique 2Go RAM for VRAM | eGPU Intel, Intel® HD Graphics 770, 32 cores, 300MHz - 1.5GHz Turbo | Adreno 660, 5nm, 792 MHz, 905 MHz Max |
| **Disque** | LITEONIT LCS-256L9S-11 256Go, 2.5", 7mm SATA 6Gb/s           | LITEONIT LCS-256L9S-11 256Go, 2.5", 7mm SATA 6Gb/s           | SOLIDIGM SSDPFKNU512GZ 512Go M.2 NVMe PCIe                   | 256Go UFS 3.0                                               |
| **Type de disque** | SSD                                                  | SSD                                                          | SSD                                                          | SSD                                                          |
| **Fichier de pagination** | Oui                                           | Oui                                                          | Oui                                                          | Non                                                          |
| **Fichier d’échange** | Oui                                               | Oui                                                          | Oui                                                          | Non                                                          |

Ces configurations matérielles ont été utilisées pour tester les différents TP (sauf sur smartphone). Il est important de noter que les performances des threads peuvent varier en fonction de la capacité de traitement parallèle de chaque machine, ce qui influence la rapidité et la fluidité de l'exécution des programmes.

On peut également souligner les différents moyens d'obtenir des informations détaillées sur le matériel des machines. Parmi les outils les plus courants, on trouve :

- **Msconfig** : un utilitaire Windows qui permet de visualiser et configurer le démarrage et certains aspects de la configuration matérielle.
- **Gestionnaire de tâches** : utile pour vérifier l'utilisation des ressources en temps réel, notamment l'usage du processeur, de la mémoire et du disque.
- **Commandes CMD** : Windows offre plusieurs commandes en ligne permettant d'obtenir des informations spécifiques sur le matériel. Par exemple, la commande `wmic memorychip get serialnumber` permet de récupérer le numéro de série de la mémoire vive (RAM), offrant ainsi plus de détails sur sa configuration.

---

## <a id="tp-1"/>3. TP 1

### <a id="diagramme-de-classe"/>3.1. Diagramme de Classe

![Diagramme TP1](https://github.com/Gascor/TP1_Mobile_src/blob/master/docs/Conception/ConceptionV1.png)

### <a id="les-classes-et-leurs-rôles"/>3.2. Les Classes et leurs Rôles

#### 3.2.1. **UneFenetre**

`UneFenetre` est l'interface principale qui gère l'affichage de l'application. Elle hérite de `JFrame`, une classe utilisée pour la création de fenêtres graphiques en Java.

#### 3.2.2. **UnMobile**

La classe `UnMobile` représente un objet mobile graphique. Son rôle est de se déplacer sur l'écran selon les paramètres définis. Il contient des méthodes pour gérer son mouvement (`run()`) et son affichage (`paintComponent()`).

#### 3.2.3. **Thread et Runnable**

L'utilisation de threads dans cette application permet de déplacer `UnMobile` de manière asynchrone, en parallèle avec l'interface graphique. En héritant de l'interface `Runnable`, `UnMobile` peut être exécuté dans un thread indépendant.

#### 3.2.4. **TpMobile**

Classe contenant la méthode `main()`, elle sert de point de départ pour lancer l'application et initialiser les composants.

### <a id="cycle-de-vie-des-threads"/>3.3. Cycle de Vie des Threads

Les **threads** passent par plusieurs états au cours de leur cycle de vie :  
1. **Nouveau** : Le thread est créé mais pas encore démarré.  
2. **Prêt** : Il est en attente de ressources pour commencer son exécution.  
3. **En cours d'exécution** : Le thread est en train d'être exécuté par le processeur.  
4. **Bloqué** : Il est en pause, en attente d'une ressource comme l'accès à un fichier ou à une section critique partagée.  
5. **Terminé** : Le thread a exécuté tout son code et ne peut plus être relancé.  

Le système d'exploitation gère la répartition des threads sur les cœurs du processeur et peut les déplacer d'un cœur à l'autre si nécessaire. Bien que nous puissions influencer leur synchronisation, l'allocation des ressources est contrôlée par l'OS.

---

## <a id="tp-2"/>4. TP 2

### <a id="tp2-diagramme-de-classe"/> 4.1. Diagramme de Classe

![Diagramme TP3bis](https://github.com/Gascor/TP1_Mobile_src/blob/master/docs/Conception/Conception_Cemaphore_V1.png)

### <a id="accès-concurrent"/>4.2. Accès Concurrent

Dans ce TP, nous avons exploré les problèmes d'accès concurrent entre plusieurs threads, notamment lorsqu'ils tentent d'accéder à une même ressource (comme une zone mémoire ou une variable partagée). Cela peut entraîner des conflits ou des erreurs si la synchronisation n'est pas gérée correctement.

### <a id="exclusion-mutuelle-et-problèmes-daffichage"/>4.3. Exclusion Mutuelle et Problèmes d'Affichage

Lorsque plusieurs threads accèdent aux mêmes ressources (comme `System.out` dans TP2), ils peuvent entrer en conflit. C'est ce qu'on appelle une **condition de course**. Pour éviter cela, il est nécessaire d'utiliser des mécanismes de **synchronisation**.

En Java, l'exclusion mutuelle peut être gérée par le mot-clé `synchronized` ou par des **verrous** comme les objets `Lock`. Cela permet de protéger les **sections critiques**, où l'accès concurrent pourrait entraîner des incohérences dans les données.

### Exclusion Mutuelle

L’**exclusion mutuelle** est un principe qui garantit qu’un seul thread peut accéder à une **section critique** à un moment donné. Cela empêche les **conditions de course** dans le cas d’accès concurrents à des ressources partagées.

Les **sémaphores** et **mutex** sont des mécanismes qui permettent de réguler cet accès :
- `wait()` force un thread à attendre qu'une ressource soit disponible.
- `notify()` réveille un thread en attente lorsque la ressource devient libre.

---

## <a id="tp-3"/>5. TP 3

### <a id="tp3-diagramme-de-classe"/>5.1. Diagramme de Classe

![Diagramme TP3](https://github.com/Gascor/TP1_Mobile_src/blob/master/docs/Conception/Conception_BAL_V1.png)

### <a id="explication-du-problème"/>5.2. Explication du Problème

Dans ce TP, j'ai implémenté un modèle **Producteur-Consommateur** en Java. L'idée était de simuler un producteur qui insère des lettres dans une boîte aux lettres (BAL) et un consommateur qui les retire de façon asynchrone. Les deux threads doivent fonctionner sans interférence, en utilisant une structure synchronisée pour éviter que l'un accède à la BAL pendant que l'autre l'utilise.

La **BAL** agit comme un tampon entre les deux threads. Le producteur utilise la méthode `deposerLettre()` pour insérer une lettre, tandis que le consommateur utilise `retirerLettre()` pour la récupérer. La synchronisation est cruciale ici pour éviter des conflits d'accès simultané à la BAL.

### <a id="53"/>5.3. Modèle Producteur-Consommateur avec Moniteur

Dans le TP3, le **moniteur** est un mécanisme essentiel qui assure l'exclusion mutuelle lors de l'accès à la **Boîte Aux Lettres** (BAL) partagée par le producteur et le consommateur. Un moniteur garantit qu'un seul thread peut entrer dans une section critique (par exemple, `depose()` ou `retrait()`), empêchant ainsi les conflits entre threads.

De plus, le moniteur utilise des **conditions** : si la BAL est pleine, le thread producteur attend que le consommateur libère de l'espace avant de déposer une lettre. À l'inverse, si la BAL est vide, le consommateur attend que le producteur dépose une nouvelle lettre avant de la retirer. Cela assure un fonctionnement asynchrone fluide sans erreur d'accès concurrent.

## <a id="tp3bis"/> 6. TP 3bis - Boulangerie avec BlockingQueue

### <a id="tp3bis-diagramme-de-classe"/> 6.1. Diagramme de Classe

![Diagramme TP3bis](https://github.com/Gascor/TP1_Mobile_src/blob/master/docs/Conception/Conception_Boulanger_V1.png)

### <a id="contexte3bis"/>6.2. Contexte du TP

Dans ce TP, nous avons implémenté une **boulangerie** avec une file d'attente bloquante (**BlockingQueue**), qui modélise un système de production et de consommation asynchrone. Ce modèle suit le schéma classique **Producteur-Consommateur** vu précédemment, où plusieurs **boulangers** produisent des **pains** et les déposent dans une file d'attente, pendant que des **mangeurs** consomment ces pains à un rythme variable.

La particularité de cette implémentation réside dans l'utilisation de l'API **Concurrent** de Java, en particulier la classe **BlockingQueue**. Cette structure simplifie la gestion de la synchronisation entre les threads producteurs et consommateurs, tout en assurant la sécurité des données partagées.

### Les Classes

- **Boulanger** : Producteur, il dépose des pains dans la file d'attente à intervalle régulier. Si la boulangerie est pleine (20 pains), il attend avant de pouvoir y déposer un nouveau pain.
  
- **Mangeur** : Consommateur, il prend des pains de la file d'attente de manière aléatoire. Si la boulangerie est vide, il attend qu'un nouveau pain soit produit. Si un **Pain Empoisonné** est consommé, il arrête son exécution.

- **Boulangerie** : Représente la file d'attente de la boulangerie. Elle utilise une **ArrayBlockingQueue** de taille fixe (20), ce qui signifie qu'elle peut contenir au maximum 20 pains à la fois. Elle offre deux méthodes principales :
  - `depose()` : Utilisée par le boulanger pour ajouter un pain à la file.
  - `achete()` : Utilisée par le mangeur pour retirer un pain de la file.
  
  La boulangerie utilise des méthodes non bloquantes, comme **`offer()`** et **`poll()`**, pour gérer respectivement les ajouts et les retraits dans la file, avec des délais d'attente maximum.

- **Pain** : Représente les pains créés et consommés. La classe contient un élément spécial, le **Pain Empoisonné**, utilisé pour arrêter les consommateurs "les tuer" une fois qu'il n'y a plus de pains à produire.

### <a id="modele3bis"/> 6.3. Modèle Producteur-Consommateur avec BlockingQueue

Le système fonctionne en continu, les boulangers produisent des pains à intervalles réguliers d'une seconde. Une fois que la boulangerie atteint sa capacité maximale (20 pains), les boulangers doivent attendre que des pains soient consommés pour en produire davantage. 

Les mangeurs, de leur côté, consomment les pains de manière aléatoire (avec un délai entre 0 et 1 seconde). Si un **Pain Empoisonné** est retiré de la boulangerie, cela signale la fin du processus, et les mangeurs arrêtent de consommer.

Cette simulation permet de comprendre et d'illustrer le rôle de **BlockingQueue** dans la gestion de la synchronisation des tâches concurrentes.

### Points Clés de l'Implémentation
1. **ArrayBlockingQueue** : Une file d'attente bloquante avec une taille fixe qui gère automatiquement la synchronisation entre les producteurs et les consommateurs.
2. **Pain Empoisonné** : Utilisé pour arrêter les mangeurs et marquer la fin de la simulation.
3. **Gestion des Délais** : Les méthodes `offer()` et `poll()` sont utilisées avec des délais pour gérer l'attente lorsque la boulangerie est pleine ou vide.
4. **Modèle Producteur-Consommateur** : Ce modèle classique est ici simplifié par l'utilisation d'une BlockingQueue, qui assure une gestion fluide des tâches concurrentes sans besoin explicite de gestion des verrous.

### Résumé du TP3bis

Grâce à l'utilisation de **BlockingQueue**. La file d'attente bloquante nous a dispensé de la gestion manuelle des verrous et des conditions de course. La simulation de la boulangerie est un exemple concret de l'importance des collections dans des environnements à **haute concurrence**.

---

### <a id="conclusion"/>7. Conclusion

Jusqu'à maintenant, le cours de **Programmation Avancée** nous a permis d'explorer en profondeur la gestion des threads et des processus en Java. Les trois TP réalisés ont démontré l'importance de la **synchronisation** et de la gestion des ressources partagées. Grâce à ces travaux pratiques, j'ai acquis une solide compréhension des mécanismes sous-jacents à la programmation concurrente, et je comprends désormais mieux l'importance de l'architecture matérielle sur l'exécution des programmes multithreadés.

---

Ce rapport présente également les concepts étudiés tout en mettant en avant différentes problématiques et des solutions mises en œuvre pour les résoudre. :)

---

> **Liens de Navigation**
>
> [Retour en haut](#compte-rendu---développement-avancé)
>
> [Voir le Diagramme de Classe du TP1](#diagramme-de-classe)
>
> [Voir le Diagramme de Classe du TP3](#tp3-diagramme-de-classe)
>
> [Voir le Diagramme de Classe du TP3bis](#tp3bis-diagramme-de-classe)
> 
> [Pour plus de détails sur le l'API Concurrent et la blocking Queue](https://blog.paumard.org/cours/java-api/chap05-concurrent-queues.html)
>
> [Doc BlockingQueue Oracle](https://igm.univ-mlv.fr/~juge/javadoc-19/java.base/java/util/concurrent/BlockingQueue.html)