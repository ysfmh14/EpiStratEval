# EpiStrat-Eval: outil d’évaluation des stratégies d’extraction d’informations spatiales pour la veille en épidémiologie
Ce projet consiste en un tableau de bord interactif développé avec Dash et Folium. Son but est de fournir une plateforme permettant la visualisation et l'analyse des données relatives aux maladies, ainsi que de permettre l'évaluation des différentes stratégies d'extraction d'informations spatiales utilisées pour la veille épidémiologique.
## Prérequis
Avant de commencer, assurez-vous d'avoir installé Python et les bibliothèques suivantes :

- Dash
- Folium
- Pandas
- Inflect
- Flask
- Dash Bootstrap Components
  
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
- Affichage des positions des détections des maladies sur une carte interactive.
- Filtre des données par pays et/ou par fenêtre temporelle.
- Affichage de la liste des hôtes extraits.
- Rafraîchissement des données en cas de modification.
- Chargement de fichiers contenant des données déjà évaluées.
## Structure du projet
- app.py : Fichier principal contenant le code de l'application Dash.
- README.md : Documentation du projet (vous êtes en train de le lire !).
## Contribuer
Les contributions sont les bienvenues ! Pour contribuer à ce projet, suivez ces étapes :

- Effectuez un fork du dépôt.
- Créez une branche pour votre fonctionnalité (git checkout -b feature/NomDeLaFonctionnalité).
- Committez vos modifications (git commit -am 'Ajouter une nouvelle fonctionnalité').
- Push votre branche sur GitHub (git push origin feature/NomDeLaFonctionnalité).
- Créez une nouvelle demande d'extraction sur GitHub.
## Auteur
- Youssef MAHDOUBI
- Sarah VALENTIN
- Najlae IDRISSI
- Mathieu ROCHE
