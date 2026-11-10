#  Tamagotchi Discord Bot

Un bot Discord interactif développé en Python permettant à chaque membre d'un serveur d'adopter, d'élever et de prendre soin de son propre animal de compagnie virtuel (Tamagotchi) directement via des commandes Slash (`/`).



##  Fonctionnalités

- **Adoption personnalisée** : Choisis ton animal parmi différentes espèces (Capybara, Chien, Chat Noir, Chauve-Souris...) et donne-lui un prénom.
- **Gestion des jauges** : Surveille la faim, l'énergie, le bonheur et la propreté de ton animal.
- **Système d'XP et Niveaux** : Fais monter ton compagnon en niveau en t'occupant de lui au quotidien.
- **Cycle automatique en arrière-plan** : La faim et l'énergie diminuent régulièrement de façon autonome (tâche asynchrone).
- **Sauvegarde persistante** : Toutes les données des joueurs et de leurs animaux sont enregistrées dans un stockage JSON structuré.



##  Commandes Slash disponibles

| Commande | Description |
| :--- | :--- |
| `/tamagotchi` | Adopte un nouveau compagnon virtuel. |
| `/profil` | Affiche l'état complet, le niveau et les jauges de ton animal. |
| `/nourrir` | Donne à manger à ton compagnon pour remonter sa faim. |
| `/jouer` | Joue avec lui pour augmenter son bonheur. |
| `/dormir` | Fais-le se reposer pour restaurer son énergie. |
| `/laver` | Nettoie ton animal pour remonter sa propreté. |
| `/kill` | Abandonne ton animal actuel pour pouvoir en adopter un nouveau. |



##  Structure du Projet

```
Project-final/
├── main.py          # Point d'entrée du bot, synchronisation des commandes
├── orders.py        # Commandes slash du jeu (Cog) et boucle automatique
├── animals.py       # Configuration des espèces et données de base
├── storage_json.py  # Fonctions de lecture/écriture de la base JSON
├── utils.py         # Fonctions utilitaires (jauges visuelles, calculs d'XP)
├── requirements.txt # Dépendances du projet
└── images/          # Images associées aux animaux
````
##  Guide d'Installation et de Lancement

Suis ces étapes simples pour faire fonctionner le bot sur ton serveur Discord :

### 1. Prérequis
- Avoir **Python 3.10** (ou une version plus récente) installé sur ton ordinateur.
- Avoir un compte **Discord** et un serveur Discord où tu as les droits d'administrateur.


### 2. Télécharger le projet
Ouvre ton terminal (ou invite de commande `cmd` / PowerShell) et clone le dépôt :
```
git clone https://github.com/ton-profil/Project-final.git
cd Project-final
