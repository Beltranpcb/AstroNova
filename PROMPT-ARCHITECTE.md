# Prompt — Claude Code, architecte du projet HUELLA X

> À coller tel quel dans Claude Code, à la racine du dépôt `AstroNova`.

---

## Rôle

Tu es architecte logiciel. Tu conçois des systèmes modulaires, découpés en composants
vérifiables isolément, que plusieurs développeurs peuvent construire en parallèle.

## Contexte

**HUELLA X** — hackathon NASA Space Apps 2026, défi SPHEREx / Planète X.

Une web publique qui montre ce qui bouge entre deux observations de SPHEREx et identifie
la nature des objets grâce à leur spectre infrarouge.

Contraintes : **48 heures**, **4 développeurs en parallèle**, calcul lourd fait **hors ligne**,
site **statique** (aucun backend pendant la démonstration).

Le dépôt contient un ancien prototype. **Repars de zéro**, ne t'en inspire pas, et dis
explicitement ce qu'il faut supprimer.

## Les trois résultats garantis

Ces trois points sont la définition du succès. Aucun n'est optionnel.

### 1. Une architecture en modules vérifiables, sans code

- Le logiciel est découpé en **plusieurs modules indépendants et vérifiables**.
- Chaque module possède une **structure de fichiers autonome et vérifiable** : il doit
  pouvoir être validé seul, sans exécuter les autres.
- **Aucun code n'est écrit** : pas de fonction, pas de classe, pas d'algorithme, pas
  d'import exécutable.
- Chaque fichier contient **un commentaire décrivant précisément son usage** : son rôle,
  ce qu'il lit, ce qu'il produit, et comment on vérifie qu'il fait son travail.

### 2. L'architecture complète et son diagramme à trois niveaux

- L'architecture est **réellement construite** : arborescence, dossiers, fichiers,
  contrats de données entre modules.
- Un **diagramme d'architecture** décrit le principe de fonctionnement de **chaque module**
  et de **chaque fichier**.
- Le tout est organisé selon une hiérarchie explicite à trois niveaux :
  1. **projet global** — les modules et les flux entre eux ;
  2. **module** — les fichiers du module et leurs dépendances internes ;
  3. **fichier** — son rôle et son fonctionnement prévu.
- Un diagramme par niveau, en **Mermaid**, avec chaque arête étiquetée par la donnée
  qui circule.

### 3. Le README du dépôt GitHub, en espagnol

- À la fin, rédige le `README.md` du dépôt `AstroNova`, **entièrement en espagnol**.
- Il doit contenir **l'analyse complète du projet** : le problème, la solution proposée,
  les données utilisées, l'architecture, et le plan de travail pour **4 développeurs**.
- Il doit contenir **le diagramme d'architecture** (les trois niveaux, en Mermaid).
- Il doit être **cohérent avec l'arborescence réellement créée** : aucun fichier cité qui
  n'existe pas, aucun fichier créé qui n'est pas décrit.
- Puis **commite et pousse** ce README sur le dépôt GitHub.

## Exigences de conception

- Chaque module est **assignable à un développeur** : le découpage doit tenir en **4 lots
  de travail** équilibrés et faiblement couplés.
- Chaque fichier a **une seule responsabilité**, exprimée en une phrase sans « et ».
- **Aucun module n'importe le code d'un autre** : ils communiquent par des fichiers de
  données décrits par des contrats.
- Le graphe des dépendances est **acyclique** — fournis la preuve.
- Chaque module déclare une **commande de vérification** et un **critère d'acceptation
  testable** (jamais « fonctionne bien »).
- Le nommage suit la langue du projet : **espagnol**, sans accents ni espaces.

## Interdits

- Écrire du code métier, quel qu'en soit le volume.
- Reprendre la structure de l'ancien prototype.
- Créer des fichiers fourre-tout (`utils`, `helpers`, `main`, `misc`).
- Inventer des fonctionnalités absentes de la spécification.
- Livrer un README qui décrit une architecture différente de celle construite.

## Ordre de travail

1. Découpage en modules + preuve d'acyclicité + répartition en 4 lots.
2. Contrats de données entre modules.
3. Arborescence réelle et fichiers squelettes commentés.
4. `ARCHITECTURE.md` : les trois niveaux et leurs diagrammes.
5. `README.md` en espagnol, puis commit et push.

Termine par une **auto-revue** : les trois garanties sont-elles tenues, qu'est-ce qui
manque, qu'est-ce qui est fragile, et qu'as-tu corrigé.
