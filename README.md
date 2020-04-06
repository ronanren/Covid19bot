# Covid19bot 🦠

# Table des matières

- [Fonctionnalités](#Fonctionnalités)
- [Enregistrement en CSV](#Enregistrement-en-CSV)
- [Message par mail](#Message-par-mail)

# Fonctionnalités

- Vérification régulier pour vérifier si les nouvelles données sont publiées
- Enregistrement des nouvelles données quotidiennes dans un CSV
- Création de 2 graphiques (statistiques total et statistiques quotidiennes)
- Création et envoi d'un message par mail des nouvelles statistiques et des 2 graphiques

Bot utilisé sur le compte twitter : [@FrenchCovid](https://twitter.com/FrenchCovid)

## Enregistrement en CSV

| Date | Total Cases | New Cases | Total Deaths | New Deaths | Total Recovered | Active Cases | Critical | New Recovered | New Active | New Critical | PlaceInWorld |
| ---- | ----------- | --------- | ------------ | ---------- | --------------- | ------------ | -------- | ------------- | ---------- | ------------ | ------------ |


fichier csv mis à jour régulièrement : [dataFrance.csv](https://github.com/ronanren/Covid19bot/blob/master/data/dataFrance.csv)

## Message par mail

#### Gestion de connexion pour l'envoi de mail :

- Modifier le fichier `config.example.py` en `config.py` avec vos identifiants gmail (si c'est autre que gmail, changer le serveur SMTP)
- Format de `config.py` :

```python
login = "mail"
password = "password"
maildestination = "mail"
```

#### exemple de message par mail :

<img src="images/exampleMail.png" width="500">
