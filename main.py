# -*- coding: UTF-8 -*-
import requests
import re
from datetime import date
import matplotlib.pyplot as plt
from math import ceil
import csv
import os
import time
import locale
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from halo import Halo
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
                tabNewCases.append(int(row[2].replace(".", "")))
                tabTotalDeaths.append(int(row[3].replace(".", "")))
                tabNewDeaths.append(int(row[4].replace(".", "")))
                tabTotalRecovered.append(int(row[5].replace(".", "")))
                tabActiveCases.append(int(row[6].replace(".", "")))
                tabCritical.append(int(row[7].replace(".", "")))
                tabNewRecovered.append(int(row[8].replace(".", "")))
                if (int(row[9].replace(".", "")) < 0):
                    tabNewActive.append(0)
                else:
                    tabNewActive.append(int(row[9].replace(".", "")))
                if (int(row[10].replace(".", "")) < 0):
                    tabNewCritical.append(0)
                else:
                    tabNewCritical.append(int(row[10].replace(".", "")))
                tabDate.append(line_count)
            line_count += 1


def makeGraph():

    os.mkdir("data/" + str(date.today()))
    # Graphe 1
    plt.plot(tabDate, tabTotalCases, "o-",
             label="Population touchée", linewidth=3, color="#9b59b6")
    plt.plot(tabDate, tabActiveCases, "o-",
             label="Population malade", linewidth=3, color="#f1c40f")
    plt.plot(tabDate, tabTotalRecovered, "o-",
             label="Population guérie", linewidth=3, color="#2ecc71")
    plt.plot(tabDate, tabCritical, "o-",
             label="Population critique", linewidth=3, color="#e74c3c")
    plt.plot(tabDate, tabTotalDeaths, "o-",
             label="Population décédée", linewidth=3, color="#2c3e50")

    plt.axis([0, numberOfDay + 1, 0, ceil(
        (int(cases[0].replace(".", ""))/5000))*5000 + 5000])
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.xlabel('Jours à partir du 17 mars 2020')
    plt.ylabel('Population')
    plt.title('Avancé du COVID-19 en France du ' +
              str(date.today().strftime("%A %d %B %Y")))
    plt.savefig('data/' + str(date.today()) +
                "/" + str(date.today()) + '_1.png')
    plt.clf()
    # Graphe 2
    plt.plot(tabDate[1:], tabNewCases[1:], "o-",
             label="Population touchée chaque jour", linewidth=3, color="#9b59b6")
    plt.plot(tabDate[1:], tabNewActive[1:], "o-",
             label="Population malade chaque jour", linewidth=3, color="#f1c40f")
    plt.plot(tabDate[1:], tabNewRecovered[1:], "o-",
             label="Population guérie chaque jour", linewidth=3, color="#2ecc71")
    plt.plot(tabDate[1:], tabNewCritical[1:], "o-",
             label="Population critique chaque jour", linewidth=3, color="#e74c3c")
    plt.plot(tabDate[1:], tabNewDeaths[1:], "o-",
             label="Population décédée chaque jour", linewidth=3, color="#2c3e50")

    plt.axis([0, numberOfDay + 1, 0, ceil(max(tabNewCases + tabNewActive +
                                              tabNewRecovered + tabNewCritical + tabNewDeaths)/1000)*1000 + 1000])

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.xlabel('Jours à partir du 18 mars 2020')
    plt.ylabel('Population')
    plt.title('Avancé du COVID-19 en France du ' +
              str(date.today().strftime("%A %d %B %Y")))
    plt.savefig('data/' + str(date.today()) +
                "/" + str(date.today()) + '_2.png')
    plt.clf()

    # Graphe 3
    index = p.text.find('id="main_table_countries_today"')
    indexEnd = index + p.text[index:].find("</table>")

    countries = re.findall(
        r'(?<=<a class="mt_a" href="country\/)(.*)(?=\/">)', str(p.text[index:indexEnd]))
    countries = [country.upper() for country in countries][:5]
    totalcases = re.findall(
        r'(?<=<\/a><\/td>\n<td style="font-weight: bold; text-align:right">)((.|\n){50})', str(p.text[index:indexEnd]))

    totalCasesCountries = []
    totalCasesCountries = (re.findall(
        r"[\d]{1,5},[\d]{3}", str(totalcases)))[:5]

    totaldeaths = re.findall(
        r'(?<=<\/a><\/td>\n<td style="font-weight: bold; text-align:right">)((.|\n){180})', str(p.text[index:indexEnd]))
    totalDeathsCountries = []

    for x in range(0, 5):
        totalDeathsCountries.append(int(re.findall(
            r"[\d]{1,5},[\d]{3}", str(totaldeaths[x][0][100:]))[0].replace(",", "")))

    for x in range(0, 5):
        totalCasesCountries[x] = int(totalCasesCountries[x].replace(",", ""))

    year = countries[::-1]
    totalcases = totalCasesCountries[::-1]
    deaths = totalDeathsCountries[::-1]

    totalcases = [totalcases[i]-deaths[i] for i in range(5)]

    bar1 = plt.barh(year, deaths, color="#2c3e50",
                    label="Population décédée", height=0.8)
    bar2 = plt.barh(year, totalcases, left=deaths,
                    color="#9b59b6", label="Population malade", height=0.8)

    plt.xlabel('Nombre total de malade et décès')
    plt.ylabel('Pays')

    plt.legend(loc='lower right')
    plt.title('Avancé du COVID-19 dans le monde du ' +
              str(date.today().strftime("%A %d %B %Y")))
    plt.savefig('data/' + str(date.today()) +
                "/" + str(date.today()) + '_3.png')
    plt.clf()


while True:

    spinner.color = 'cyan'
    spinner.text = 'Scrapping des données'
    # Parsing des données sur worldometers.info
    p = requests.get('https://www.worldometers.info/coronavirus/')

    indexFrance = p.text.find(
        '<a class="mt_a" href="country/france/">France</a>')
    indexFranceEnd = indexFrance + p.text[indexFrance:].find("</tr>")

    PlaceInWorld = p.text[:indexFranceEnd].count('href="country/')

    cases = re.findall(
        r'[\d]{1,3}.[\d]{3}|\d+', str(p.text[indexFrance:indexFranceEnd]).replace(",", "."))
    data = ["Total Cases", "New Cases", "Total Deaths",
            "New Deaths", "Total Recovered", "Active Cases", "Critical"]
    numberOfDay = (date.today()-date(2020, 3, 16)).days

    verif = False

    # Changer les données manuellements si il y a des erreurs au niveau de la source
    # cases[0] = 0 # Cas totaux
    # cases[1] = 0 # nouveaux cas
    # cases[2] = 0 # morts totaux
    # cases[3] = 0 # nouveaux morts
    # cases[4] = 0 # guéris totaux
    # cases[5] = 0 # malades 
    # cases[6] = 0 # cas critique/en réanimation
    # cases[7] = 0 # nouveaux guéris
    # cases[8] = 0 # nouveaux malades
    # cases[9] = 0 # nouveaux critique/en réanimation
    # cases[10] = 0 # place dans le monde
    # cases[11] = 0 # tests totaux
    # cases[12] = 0 # nouveaux tests

    # Retrouver les données d'hier
    f1 = open("data/dataFrance.csv", "r")
    last_line = f1.readlines()[-1].split(',')
    f1.close()
    try:
        # Vérifier si toutes les données sont publiées
        if (last_line[0] != str(date.today()) and cases[10] and int(cases[6].replace(".", "")) != int(last_line[7].replace(".", ""))):
            verif = True
        else:
            spinner.color = 'magenta'
            spinner.text = 'Données déjà publiées ' + \
                time.strftime("%H:%M:%S")
    except:
        spinner.text = 'Données pas encore publiées ' + time.strftime("%H:%M:%S")

    if (verif):

        newRecovered = int(cases[4].replace(".", "")) - \
            int(last_line[5].replace(".", ""))
        newCritical = int(cases[6].replace(".", "")) - \
            int(last_line[7].replace(".", ""))
        newActive = int(cases[5].replace(".", "")) - \
            int(last_line[6].replace(".", ""))
        newTests = int(cases[9].replace(".", "")) - \
            int(last_line[12].replace(".", ""))

        # Pourcentage des nouveaux cas comparés au cas d'hier
        newRecoveredPercent = round(
            100 * (int(newRecovered)/int(last_line[8].replace(".", ""))), 2)
        newActivePercent = round(
            100 * (int(newActive)/int(last_line[9].replace(".", ""))), 2)
        newCriticalPercent = round(
            100 * (int(newCritical)/int(last_line[10].replace(".", ""))), 2)
        newDeathPercent = round(
            100 * (int(cases[3].replace(".", ""))/int(last_line[4].replace(".", ""))), 2)

        # Enregistrer les données dans le CSV
        f = open("data/dataFrance.csv", "a+")
        f.write(str(date.today()) + "," + cases[0] + "," + cases[1] +
                "," + cases[2] + "," + cases[3] + "," + cases[4] + "," + cases[5] + "," + cases[6] + "," + str(newRecovered) + "," + str(newActive) + "," + str(newCritical) + "," + str(PlaceInWorld) + "," + cases[9] + "," + str(newTests) + "\n")
        f.close()

        makeTabOfData()
        makeGraph()

        # Envoyer le message pour le tweeter
        msg = MIMEMultipart()
        msg['Subject'] = 'Data bot'
        ligne1 = "La 🇫🇷 est " + str(PlaceInWorld) + "ème au 🌎\n"
        ligne2 = "🟢 " + cases[4].replace(".", ",") + " guéris +" + str(
            newRecovered) + " [" + str(newRecoveredPercent) + "%]\n"
        if (newActive < 0):
            ligne3 = "🟠 " + cases[5].replace(".", ",") + " malades " + str(
                newActive) + " [" + str(newActivePercent) + "%]\n"
        else:
            ligne3 = "🟠 " + cases[5].replace(".", ",") + " malades +" + str(
                newActive) + " [" + str(newActivePercent) + "%]\n"
        if (newCritical < 0):
            ligne4 = "🔴 " + cases[6].replace(".", ",") + " cas graves " + str(
                newCritical) + " [" + str(newCriticalPercent) + "%]\n"
        else:
            ligne4 = "🔴 " + cases[6].replace(".", ",") + " cas graves +" + str(
                newCritical) + " [" + str(newCriticalPercent) + "%]\n"
        ligne5 = "⚫ " + cases[2].replace(".", ",") + " décès +" + cases[3].replace(
            ".", "") + " [" + str(newDeathPercent) + "%]\n"
        ligne6 = "💉 " + \
            cases[9].replace(".", ",") + " tests +" + str(newTests) + "\n\n"
        ligne7 = cases[0].replace(".", ",") + \
            " cas totaux +" + cases[1].replace(".", "")
        ligne8 = "\n\nGraphiques📈⏬\n#ConfinementJour" + str(numberOfDay)
        message = ligne1 + ligne2 + ligne3 + ligne4 + ligne5 + \
            ligne6 + ligne7 + ligne8 + "\n📈Évolution du #COVID19 en 🇫🇷"
        msg.attach(MIMEText(message))

        mailserver = smtplib.SMTP(config.server, config.port)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()

        maillogin = config.login
        mailpassword = config.password
        maildestination = config.maildestination

        mailserver.login(maillogin, mailpassword)
        mailserver.sendmail(maillogin, maildestination, msg.as_string())
        mailserver.quit()
        spinner.succeed('Données envoyés ' + time.strftime("%H:%M:%S"))
        spinner.start()
    time.sleep(30)
