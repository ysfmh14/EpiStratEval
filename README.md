# EpiStrat-Eval: outil d’évaluation des stratégies d’extraction d’informations spatiales pour la veille en épidémiologie
Ce projet est un tableau de bord interactif construit avec Dash et Folium pour visualiser et analyser les données relatives aux maladies et à leur propagation dans différentes localisations.

## Prérequis
Avant de commencer, assurez-vous d'avoir installé Python et les bibliothèques suivantes :

Dash
Folium
Pandas
Inflect
Flask
Dash Bootstrap Components
Vous pouvez installer ces bibliothèques à l'aide de pip :
```python
pip install dash folium pandas inflect Flask dash-bootstrap-components
```
## Configuration
Clonez ce dépôt sur votre machine :
```python
git clone https://github.com/votre-utilisateur/nom-du-depot.git
```
Assurez-vous que vous êtes dans le répertoire du projet :
```python
cd nom-du-depot
```
Lancez l'application en exécutant le fichier app.py :
```python
python app.py
```
Ouvrez votre navigateur et accédez à l'URL http://127.0.0.1:8060/ pour voir le tableau de bord.
## Fonctionnalités
Affichage des données de localisation et de propagation des maladies sur une carte interactive.
Sélection de pays et de dates pour filtrer les données affichées.
Téléchargement des données filtrées au format Excel.
Gestion des validations des localisations et des articles via des boutons interactifs.
Structure du projet
### app.py : Fichier principal contenant le code de l'application Dash.
### README.md : Documentation du projet (vous êtes en train de le lire !).
location_extracted_information_S2.xlsx : Fichier de données contenant les informations sur les maladies (échantillon 1).
location_extracted_information_S5.xlsx : Fichier de données contenant les informations sur les maladies (échantillon 2).
## Contribuer
Les contributions sont les bienvenues ! Pour contribuer à ce projet, suivez ces étapes :

Effectuez un fork du dépôt.
Créez une branche pour votre fonctionnalité (git checkout -b feature/NomDeLaFonctionnalité).
Committez vos modifications (git commit -am 'Ajouter une nouvelle fonctionnalité').
Push votre branche sur GitHub (git push origin feature/NomDeLaFonctionnalité).
Créez une nouvelle demande d'extraction sur GitHub.
## Auteur
