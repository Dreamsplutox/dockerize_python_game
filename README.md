# dockerize-everything-test
Répertoire test pour le projet docker + appli python, parfait pour ne pas faire du bullshit sur le repo principal ;)

## Descriptif du projet
Pour ce projet nous avons réalisé une application python ou plus précisément un jeu avec la librairie pygame avec une interaction avec une base de données postgresql pour afficher différents messages textuels dans le jeu.
Dans ce jeu, le joueur incarne un soldat qui doit vaincre les goblins qui envahissent sa prairie en utilisant sa fidèle arme tireuse de balles perforantes ! Saurez-vous repoussez l'invasion gobline ?

### Choix effectués par l'équipe durant le projet
* 07/07 Utiliser une base de données postgresql pour stocker des messages utilisables dans l'application
* 08/08 lorem ipsum lorem ipsum lorem ipsum

### Environnement Python
Comme dit précédemment nous avons utilisé python pour réaliser ce projet avec notamment la librairie pygame, voici les différentes étapes à réaliser pour utiliser l'environnement python que nous avons mis en place pour faire fonctionner le jeu : 

#### Créer l'environment
> py -m create venv .venv

#### Démarrer Environment
> Démarrer start.bat ;)

#### Installer les pré-requis
> pip install -r requirements.txt

## Versionning

### Workflow choisi
> Nous avons fait le choix du workflow feature branch car nous sommes des développeurs de même niveau travaillant dans une petite équipe, nous nous connaissons assez bien pour ne pas prendre de décisions à la légère et nous nous consultons entre nous via mail ou discord avant de réaliser des commits sur master ou tout simplement pour tenir l'équipe au courant de notre travail.

### Les conventions à respecter
* Chaque fonctionnalité de notre projet est réalisée sur une branche à part entière, on ne développe pas directement sur master
* Quand une fonctionnalité est terminée et testée, prévenir les autres membres du groupe avant de la push sur master (via discord)
* Faire des commits clairs et concis ne dépassant pas 200 caractères, ne contenant pas de mots écrits uniquement en majuscules et commençant toujours par un mot clé ou un groupe de mots clés résumant le commit
* Structurer le repo en mettant bien chaque fichier dans des dossiers adaptés, il ne faut pas que des fichiers .bat, .py ou autre "vagabondent" dans le repo
class ou autre trainent sur le dépôt 
## Fonctionnalités de l'application
* Décor de jeu avec musiques et bruitages
* Jouer un personnage 
* Possibilité de tirer des balles
* Présence d'un personnage ennemi
* Règles codées pour mettre fin au jeu (victoire / défaite)
* Liaison avec une base postgresql pour afficher des messages au joueur

## Déploiement
Pour déployer l'application en production avec Docker manuellement, vous devez tout d'abord créer un conteneur pour la base de données postgresql en suivant les instructions ci-dessous : 
### Conteneur postgresql
1) docker network create postgres_for_python
2) docker pull postgres:11-alpine
3) docker volume create postgres_for_python_dbdata
4) docker run --name postgres_for_python_db --network=postgres_for_python -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -v postgres_for_python_dbdata:/var/lib/postgresql/data -p 5433:5433 -d postgres:11-alpine
### Création de la base
1) docker exec -it postgres_for_python_db psql -U postgres
2) CREATE DATABASE python_game_data;
3) \c python_game_data
4) CREATE TABLE game_text(id SERIAL PRIMARY KEY, text_name VARCHAR(255) UNIQUE NOT NULL, text_content
VARCHAR(255) NOT NULL);
5) INSERT INTO game_text (text_name, text_content) values ('description', 'Vous devez affronter le goblin et obtenir un maximum de points, bonne chance !');
6) INSERT INTO game_text (text_name, text_content) values ('game_over', 'Vous êtes mort trop de fois, fin de la partie !');
7) INSERT INTO game_text (text_name, text_content) values ('win', 'Vous avez survecu aux attaques des goblins, felicitations !');
### Conteneur python
1) Pour utiliser notre application python, nous avons besoin d'installer un serveur X en utilisant ce tutoriel https://cuneyt.aliustaoglu.biz/en/running-gui-applications-in-docker-on-windows-linux-mac-hosts/
2) Activer le serveur X, et démarrer le Dockerfile du projet avec la commande :
 docker build -t appli_python .
3) Il faut ensuite run l'application en précisant l'adresse du serveur X:
 docker run --rm -it -e DISPLAY=192.168.56.1:0.0 python_app



