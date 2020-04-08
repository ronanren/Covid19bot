# Covid19bot 🦠

<h4 align="center">🤖 Bot permettant de donner chaque jour les statistiques du COVID-19 en France</h4>

<p align="center">
  <a href="#Fonctionnalités">Fonctionnalités</a> |
  <a href="#Utilisation">Utilisation</a> |
  <a href="#Enregistrement-en-CSV">Enregistrement en CSV</a> |
  <a href="#Message par mail">Message par mail</a> |
  <br>
  <a href="https://www.ronanren.github.io">Consultez mon site personnel !</a> 
</p>
<img src="images/console.gif" width="400" style="display: block;
  margin-left: auto;
  margin-right: auto;">

Bot utilisé sur le compte twitter : [@FrenchCovid](https://twitter.com/FrenchCovid)

# Fonctionnalités

- Vérification régulière en intervalle de temps pour vérifier si les nouvelles données sont publiées
- Enregistrement des nouvelles données quotidiennes dans un CSV
- Création de 3 graphiques (statistiques total, statistiques quotidiennes et statistiques mondiales des 5 premiers pays les plus touchés)
- Création et envoi d'un message par mail des nouvelles statistiques pour tweeter

# Utilisation

```bash
# Cloner ce dépôt
$ git clone https://github.com/ronanren/Covid19bot

# Accéder au dossier
$ cd Covid19bot

# Installer les dépendances
$ pip install requirements.txt

# Modifier config.py
login = "mail"
password = "password"
maildestination = "mail"
server = "server smtp"
port = 587

# Lancer le script
$ python main.py
```

# Enregistrement en CSV

**Voici les données enregistrées au sein du CSV [dataFrance.csv](https://github.com/ronanren/Covid19bot/blob/master/data/dataFrance.csv)**

### Parsing des données sur [Worldometers.info](https://www.worldometers.info/coronavirus/)

| Date | Total Cases | New Cases | Total Deaths | New Deaths | Total Recovered | Active Cases | Critical | New Recovered | New Active | New Critical | PlaceInWorld | Total tests | New Tests |
| ---- | ----------- | --------- | ------------ | ---------- | --------------- | ------------ | -------- | ------------- | ---------- | ------------ | ------------ | ----------- | --------- |


# Message par mail

**Les pourcentages présentent l'évolution des chiffres par rapport aux chiffres de la veille.**

### exemple de message reçu par mail :

<img src="images/exampleMail.png" width="500">
