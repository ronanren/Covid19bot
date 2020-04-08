# Covid19bot 🦠

<h4 align="center">🤖 Bot permettant de donner chaque jour les statistiques du COVID-19 en France</h4>

<p align="center">
<a href="https://badge.fury.io/py/requests"><img src="https://badge.fury.io/py/requests.svg" alt="PyPI version" height="18"></a>
  <a href="https://badge.fury.io/py/matplotlib"><img src="https://badge.fury.io/py/matplotlib.svg" alt="PyPI version" height="18"></a>
  <a href="https://badge.fury.io/py/halo"><img src="https://badge.fury.io/py/halo.svg" alt="PyPI version" height="18"></a>
  <a href="https://badge.fury.io/py/csv"><img src="https://badge.fury.io/py/csv.svg" alt="PyPI version" height="18"></a>
</p>

<p align="center">
  <a href="#Fonctionnalités">Fonctionnalités</a> |
  <a href="#Utilisation">Utilisation</a> |
  <a href="#Enregistrement-en-CSV">Enregistrement en CSV</a> |
  <a href="#Message-par-mail">Message par mail</a> |
  <a href="#Licence">Licence</a> |
  <a href="#Contactez-moi">Contactez-moi</a> |
  <br>
  <a href="https://ronanren.github.io" target="_blank">Consultez mon site personnel !</a> 
</p>

<p align="center">
    <img src="images/console.gif" width="400">
</p>

Bot utilisé sur le compte twitter : <a href="https://twitter.com/FrenchCovid" target="_blank">@FrenchCovid</a>

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

# Modifier le fichier config.py
login = "mail"
password = "password"
maildestination = "mail"
server = "server smtp"
port = 587

# Lancer le script
$ python main.py
```

# Enregistrement en CSV

**Voici les données enregistrées au sein du CSV <a href="https://github.com/ronanren/Covid19bot/blob/master/data/dataFrance.csv" target="_blank">dataFrance.csv</a>**

### Parsing des données sur <a href="https://www.worldometers.info/coronavirus/" target="_blank">Worldometers.info</a>

| Date | Total Cases | New Cases | Total Deaths | New Deaths | Total Recovered | Active Cases | Critical | New Recovered | New Active | New Critical | PlaceInWorld | Total tests | New Tests |
| ---- | ----------- | --------- | ------------ | ---------- | --------------- | ------------ | -------- | ------------- | ---------- | ------------ | ------------ | ----------- | --------- |


# Message par mail

**Les pourcentages présentent l'évolution des chiffres par rapport aux chiffres de la veille.**

### exemple de message reçu par mail :

<img src="images/exampleMail.png" width="500">

# Licence

MIT

# Contactez-moi

**Twitter** : <a href="https://twitter.com/Ronanren" target="_blank">@Ronanren</a>
