# -*- coding: UTF-8 -*-
import requests
import re
import datetime
import matplotlib.pyplot as plt
from math import ceil
import csv
import time
import locale
from halo import Halo
import tweepy
import config


# Mettre les dates en francais
locale.setlocale(locale.LC_TIME, '')

spinner = Halo(text='Scrapping des données', spinner='dots', color='cyan')
spinner.start()


def makeTabOfData():
    global tabDate, tabTotalCases, tabNewCases, tabTotalDeaths, tabNewDeaths, tabTotalRecovered, tabActiveCases, tabCritical, tabNewRecovered, tabNewActive, tabNewCritical
    tabTotalCases = []
    tabNewCases = []
    tabTotalDeaths = []
    tabNewDeaths = []
    tabTotalRecovered = []
    tabActiveCases = []
    tabCritical = []
    tabNewRecovered = []
    tabNewActive = []
    tabNewCritical = []
    tabDate = []
    with open('data/dataFrance.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                tabTotalCases.append(int(row[1].replace(".", "")))
                tabTotalDeaths.append(int(row[3].replace(".", "")))
                tabNewDeaths.append(int(row[4].replace(".", "")))
                tabTotalRecovered.append(int(row[5].replace(".", "")))
                tabActiveCases.append(int(row[6].replace(".", "")))
                tabCritical.append(int(row[7].replace(".", "")))
                tabNewRecovered.append(int(row[8].replace(".", "")))
                tabNewActive.append(int(row[9].replace(".", "")))   
                tabNewCritical.append(int(row[10].replace(".", "")))
                tabNewCases.append(int(row[2].replace(".", "")))
                tabDate.append(line_count)
            line_count += 1


def makeGraph():

    # Graphe 1
    #plt.plot(tabDate, tabTotalCases, "-", label="Population touchée", linewidth=3, color="#9b59b6")
    plt.plot(tabDate, tabActiveCases, "-", label="Population malade", linewidth=3, color="#f1c40f")
    plt.plot(tabDate, tabTotalRecovered, "-", label="Population guérie", linewidth=3, color="#2ecc71")
    plt.plot(tabDate, tabCritical, "-", label="Population critique", linewidth=3, color="#e74c3c")
    plt.plot(tabDate, tabTotalDeaths, "-", label="Population décédée", linewidth=3, color="#2c3e50")

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.xlabel('Jours à partir du 17 mars 2020')
    plt.title('Avancé du COVID-19 en France du ' + str(datetime.datetime.today().strftime("%A %d %B %Y")))
    plt.savefig('data/franceTotal.png')
    plt.clf()

    # Graphe 2
    #plt.plot(tabDate[1:], tabNewCases[1:], "-", label="Population touchée chaque jour", linewidth=3, color="#9b59b6")
    plt.plot(tabDate[1:], tabNewActive[1:], "-", label="Population malade chaque jour", linewidth=3, color="#f1c40f")
    plt.plot(tabDate[1:], tabNewRecovered[1:], "-", label="Population guérie chaque jour", linewidth=3, color="#2ecc71")
    plt.plot(tabDate[1:], tabNewCritical[1:], "-", label="Population critique chaque jour", linewidth=3, color="#e74c3c")
    plt.plot(tabDate[1:], tabNewDeaths[1:], "-", label="Population décédée chaque jour", linewidth=3, color="#2c3e50")

    plt.legend(loc='best')
    plt.grid(True)
    plt.xlabel('Jours à partir du 18 mars 2020')
    plt.title('Avancé du COVID-19 en France du ' + str(datetime.datetime.today().strftime("%A %d %B %Y")))
    plt.savefig('data/franceToday.png')
    plt.clf()

    # Graphe 3
    nbrCountries = 8
    index = p.text.find('id="main_table_countries_today"')
    indexEnd = index + p.text[index:].find("</table>")

    countries = re.findall(r'(?<=<a class="mt_a" href="country\/)(.*)(?=\/">)', str(p.text[index:indexEnd]))
    countries = [country.upper() for country in countries][:nbrCountries]
    totalcases = re.findall(r'(?<=<\/a><\/td>\n<td style="font-weight: bold; text-align:right">)((.|\n){50})', str(p.text[index:indexEnd]))

    totalCasesCountries = []
    totalCasesCountries = (re.findall(r"[\d]{2,3},[\d]{3}|[\d]{1,3},[\d]{3},[\d]{3}", str(totalcases)))[:nbrCountries]

    totaldeaths = re.findall(r'(?<=<\/a><\/td>\n<td style="font-weight: bold; text-align:right">)((.|\n){180})', str(p.text[index:indexEnd]))
    totalDeathsCountries = []

    totalRecovered = re.findall(r'(?<=<\/a><\/td>\n<td style="font-weight: bold; text-align:right">)((.|\n){380})', str(p.text[index:indexEnd]))
    totalRecoveredCountries = []

    for x in range(0, nbrCountries):
        indexRecovered = str(totalRecovered[x]).find('<td style="font-weight: bold; text-align:right">')
        totalRecovered[x] = str(totalRecovered[x]).replace("N/A", "0,000")
        totalRecoveredCountries.append(int(re.findall(r"[\d]{1,2},[\d]{3},[\d]{3}|[\d]{1,5},[\d]{3}|[\d]{1,3}", str(
            totalRecovered[x])[indexRecovered+48:indexRecovered+70])[0].replace(",", "")))

    for x in range(0, nbrCountries):
        totalDeathsCountries.append(int(re.findall(
            r"[\d]{1,5},[\d]{3}|[\d]{1,3}", str(totaldeaths[x][0][100:]))[0].replace(",", "")))

    for x in range(0, nbrCountries):
        totalCasesCountries[x] = int(totalCasesCountries[x].replace(",", ""))

    year = countries[::-1]
    totalcases = totalCasesCountries[::-1]
    deaths = totalDeathsCountries[::-1]
    recovered = totalRecoveredCountries[::-1]

    totalcases = [totalcases[i]-deaths[i] for i in range(nbrCountries)]

    bar1 = plt.barh(year, deaths, color="#2c3e50", label="Population décédée", height=0.8)
    bar2 = plt.barh(year, totalcases, left=deaths, color="#9b59b6", label="Population touchée", height=0.8)
    bar3 = plt.barh(year, recovered, color="#27ae60", label="Population guérie", height=0.4, align='edge')

    plt.legend(loc='lower right')
    plt.ticklabel_format(style='plain', axis='x')
    plt.xticks(fontsize=7.5, rotation=35, ha="right")
    plt.title('Avancé du COVID-19 dans le monde du ' + str(datetime.datetime.today().strftime("%A %d %B %Y")))
    plt.savefig('data/global.png')
    plt.clf()


while True:

    if (datetime.datetime.now().hour >= 19 and datetime.datetime.now().hour <= 23):

        spinner.color = 'cyan'
        spinner.text = 'Scrapping des données'
        # Parsing des données sur worldometers.info
        p = requests.get('https://www.worldometers.info/coronavirus/')

        indexFrance = p.text.find('<a class="mt_a" href="country/france/">France</a>')
        indexFranceEnd = indexFrance + p.text[indexFrance:].find("</tr>")

        PlaceInWorld = p.text[:indexFranceEnd].count('href="country/')

        cases = re.findall(r'[\d]{1,2}.[\d]{3}.[\d]{3}|[\d]{1,3}.[\d]{3}|\d+', str(p.text[indexFrance:indexFranceEnd]).replace(",", ".").replace("background-color:#c8e6c9; color:#000", ""))
        data = ["Total Cases", "New Cases", "Total Deaths",
                "New Deaths", "Total Recovered", "Active Cases", "Critical", "New Recovered",
                "New Active", "New Critical", "PlaceInWorld", "Total Tests", "New Tests"]

        numberOfDay = (datetime.datetime.today()-datetime.datetime(2020, 3, 16)).days
        numberOfDayDeconfinement = (datetime.datetime.today()-datetime.datetime(2020, 5, 10)).days

        verif = False

        # Changer les données manuellements si il y a des erreurs au niveau de la source
        # cases[0] = 0 # Cas totaux
        # cases[1] = 0 # nouveaux cas
        # cases[2] = 0 # morts totaux
        # cases[3] = 0 # nouveaux morts
        # cases[4] = 0 # guéris totaux
        # cases[5] = 0 # New Recovered| Not used here
        # cases[6] = 0 # malades
        # cases[7] = 0 # cas critique/en réanimation
        # cases[8] = 0 # nouveaux guéris| Not used here
        # cases[9] = 0 # nouveaux malades| Not used here
        # cases[10] = 0 # nouveaux critique/en réanimation

        #cases.insert(index, 'valeur')

        # Retrouver les données d'hier
        f1 = open("data/dataFrance.csv", "r")
        last_line = f1.readlines()[-1].split(',')
        f1.close()

        try:
            # Vérifier si toutes les données sont publiées
            if (last_line[0] != str("20" + datetime.datetime.today().strftime("%y-%m-%d")) and cases[15]):
                verif = True
            else:
                spinner.color = 'magenta'
                spinner.text = 'Données déjà publiées ' + time.strftime("%H:%M:%S")
        except:
            spinner.text = 'Données pas encore publiées ' + time.strftime("%H:%M:%S")

        if (verif):

            newRecovered = int(cases[4].replace(".", "")) - int(last_line[5].replace(".", ""))
            newCritical = int(cases[7].replace(".", "")) - int(last_line[7].replace(".", ""))
            newActive = int(cases[6].replace(".", "")) - int(last_line[6].replace(".", ""))
            newTests = int(cases[10].replace(".", "")) - int(last_line[12].replace(".", ""))

            # Pourcentage des nouveaux cas comparés au cas d'hier
            newActivePercent = round(100 * (int(newActive)/int(last_line[9].replace(".", ""))), 2)
            newDeathPercent = round(100 * (int(cases[3].replace(".", ""))/int(last_line[4].replace(".", ""))), 2)

            if (int(last_line[8].replace(".", "")) == 0):
                newRecoveredPercent = round(100 * (int(newRecovered)), 2)
            else:
                newRecoveredPercent = round(100 * (int(newRecovered)/int(last_line[8].replace(".", ""))), 2)

            if (int(last_line[10].replace(".", "")) == 0):
                newCriticalPercent = round(100 * (int(newCritical)), 2)
            else:
                newCriticalPercent = round(100 * (int(newCritical)/int(last_line[10].replace(".", ""))), 2)

            
            # Enregistrer les données dans le CSV
            f = open("data/dataFrance.csv", "a+")
            f.write(str("20" + datetime.datetime.today().strftime("%y-%m-%d")) + "," + cases[0] + "," + cases[1] + "," + cases[2] + "," + cases[3] + "," + cases[4] + "," + cases[6] + "," + cases[7] + "," + str(newRecovered) + "," + str(newActive) + "," + str(newCritical) + "," + str(PlaceInWorld) + "," + cases[10] + "," + str(newTests) + "\n")
            f.close()

            makeTabOfData()
            makeGraph()

            # Message à tweeter
            ligne1 = "La 🇫🇷 est " + str(PlaceInWorld) + "ème au 🌎\n"
            ligne2 = "🟢 " + cases[4].replace(".", ",") + " guéris +" + str(newRecovered) + " [" + str(newRecoveredPercent) + "%]\n"
            if (newActive < 0):
                ligne3 = "🟠 " + cases[6].replace(".", ",") + " malades " + str(newActive) + " [" + str(newActivePercent) + "%]\n"
            else:
                ligne3 = "🟠 " + cases[6].replace(".", ",") + " malades +" + str(newActive) + " [" + str(newActivePercent) + "%]\n"
            if (newCritical < 0):
                ligne4 = "🔴 " + cases[7].replace(".", ",") + " cas graves " + str(newCritical) + " [" + str(newCriticalPercent) + "%]\n"
            else:
                ligne4 = "🔴 " + cases[7].replace(".", ",") + " cas graves +" + str(newCritical) + " [" + str(newCriticalPercent) + "%]\n"
            ligne5 = "⚫ " + cases[2].replace(".", ",") + " décès +" + cases[3].replace(
                ".", "") + " [" + str(newDeathPercent) + "%]\n"
            if (newTests > 0):
                ligne6 = "💉 " + cases[10].replace(".", ",") + " tests +" + str(newTests) + "\n\n"
            else:
                ligne6 = "\n\n"
            ligne7 = cases[0].replace(".", ",") + " cas totaux +" + cases[1].replace(".", "")
            ligne8 = "\n\nGraphiques📈⏬\n#DeconfinementJour" + str(numberOfDayDeconfinement)
            message = ligne1 + ligne2 + ligne3 + ligne4 + ligne5 + ligne6 + ligne7 + ligne8 
            
            consumer_key = config.consumer_key
            consumer_secret = config.consumer_secret
            access_token = config.access_token
            access_token_secret = config.access_token_secret

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth)

            api.update_status(message)
            lastIdTweet = api.user_timeline(count=1)[0].id

            image1 = "data/franceTotal.png"
            image2 = "data/franceToday.png"
            image3 = "data/global.png"
            images = (image1, image2, image3)
            media_ids = [api.media_upload(i).media_id_string for i in images]
            api.update_status(status="📈Évolution du #COVID19 en 🇫🇷", media_ids=media_ids, in_reply_to_status_id=lastIdTweet)
            spinner.succeed('Données envoyés ' + time.strftime("%H:%M:%S"))
            spinner.start()
    else:
        spinner.text = "Pas encore l'heure pour check " + time.strftime("%H:%M:%S")
    time.sleep(300)
