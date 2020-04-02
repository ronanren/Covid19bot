# -*- coding: UTF-8 -*-
import requests
import re
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import csv, os
import time
import locale
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Mettre les dates en francais
locale.setlocale(locale.LC_TIME, '')


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
                tabNewActive.append(int(row[9].replace(".", "")))
                tabNewCritical.append(int(row[10].replace(".", "")))
                tabDate.append(line_count)
                line_count += 1
            else:
                line_count += 1


def makeGraph():
    # Graphique 1
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
        (int(cases[0].replace(".", ""))/5000))*5000])
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.xlabel('Jours à partir du 17 mars 2020')
    plt.ylabel('Population')
    plt.title('Avancé du COVID-19 en France du ' +
              str(date.today().strftime("%A %d %B %Y")))
    plt.savefig('data/' + str(date.today()) + '_1.png')
    plt.clf()
    # Graphique 2
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
    

    plt.axis([0, numberOfDay + 1, 0, ceil(max(tabNewCases + tabNewActive + tabNewRecovered + tabNewCritical + tabNewDeaths)/1000)*1000])

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.xlabel('Jours à partir du 18 mars 2020')
    plt.ylabel('Population')
    plt.title('Avancé du COVID-19 en France du ' +
              str(date.today().strftime("%A %d %B %Y")))
    plt.savefig('data/' + str(date.today()) + '_2.png')
    plt.clf()


while True:
    p = requests.get('https://www.worldometers.info/coronavirus/')

    indexFrance = p.text.find(
        '<a class="mt_a" href="country/france/">France</a>')
    indexFranceEnd = indexFrance + p.text[indexFrance:].find("</tr>")

    PlaceInWorld = p.text[:indexFranceEnd].count('href="country/') + 1

    cases = re.findall(r'[\d]{1,3}.[\d]{3}|\d{3}', str(
        p.text[indexFrance:indexFranceEnd]).replace(",", "."))
    data = ["Total Cases", "New Cases", "Total Deaths",
            "New Deaths", "Total Recovered", "Active Cases", "Critical"]
    numberOfDay = (date.today()-date(2020, 3, 16)).days

    verif = False

    # Get the last date in dataFrance.csv
    f1 = open("data/dataFrance.csv", "r")
    last_date = f1.readlines()[-1].split(',')[0]
    f1.close()

    try:
        if (cases[6] and last_date != str(date.today())):
            verif = True
        else:
            print(time.strftime("%H:%M:%S") + " données déja postées ")
    except:
        print(time.strftime("%H:%M:%S") + " données pas encore postées ")

    if (verif):
        # retrieve yesterday's data
        f1 = open("data/dataFrance.csv", "r")
        last_line = f1.readlines()[-1].split(',')
        f1.close()
        newRecovered = int(cases[4].replace(".", "")) - int(last_line[5].replace(".", ""))
        newCritical = int(cases[6].replace(".", "")) - int(last_line[7].replace(".", ""))
        newActive = int(cases[5].replace(".", "")) - int(last_line[6].replace(".", ""))
    
        # percentage of new cases compared to yesterday's case
        newRecoveredPercent = round(100 * (int(newRecovered)/int(last_line[8].replace(".", ""))), 2)
        newActivePercent = round(100 * (int(newActive)/int(last_line[9].replace(".", ""))), 2)
        newCriticalPercent = round(100 * (int(newCritical)/int(last_line[10].replace(".", ""))), 2)
        newDeathPercent = round(100 * (int(cases[3].replace(".", ""))/int(last_line[4].replace(".", ""))), 2)

        # Save data in csv file
        f = open("data/dataFrance.csv", "a+")
        f.write(str(date.today()) + "," + cases[0] + "," + cases[1] +
                "," + cases[2] + "," + cases[3] + "," + cases[4] + "," + cases[5] + "," + cases[6] + "," + str(newRecovered) + "," + str(newActive) + "," + str(newCritical) + "," + str(PlaceInWorld) + "\n")
        f.close()

        makeTabOfData()
        makeGraph()

        # Send message to tweet
        msg = MIMEMultipart()
        msg['From'] = 'mail@gmail.com'
        msg['To'] = 'mail@gmail.com'
        msg['Subject'] = 'Data bot'
        ligne1 = "La 🇫🇷 est " + str(PlaceInWorld) + "ème au 🌎\n"
        ligne2 = "🟢 " + cases[4].replace(".", ",") + " guéris +" + str(newRecovered) + " [" + str(newRecoveredPercent) + "%]\n"
        ligne3 = "🟠 " + cases[5].replace(".", ",") + " malades +" + str(newActive) + " [" + str(newActivePercent) + "%]\n"
        ligne4 = "🔴 " + cases[6].replace(".", ",") + " cas graves +" + str(newCritical) + " [" + str(newCriticalPercent) + "%]\n"
        ligne5 = "⚫ " + cases[2].replace(".", ",") + " décès +" + cases[3].replace(".", ",") + " [" + str(newDeathPercent) + "%]\n\n"
        ligne6 = cases[0].replace(".", ",") + " cas totaux +" + cases[1].replace(".", "")
        ligne7 = "\n\nGraphiques📈⏬\n#ConfinementJour" + str(numberOfDay)
        message = ligne1 + ligne2 + ligne3 + ligne4 + ligne5 + ligne6 + ligne7
        msg.attach(MIMEText(message))

        # Attach graphic to message
        imgurl1 = "data/" + str(date.today()) + "_1.png"
        imgurl2 = "data/" + str(date.today()) + "_2.png"
        img_data = open(imgurl1, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(imgurl1))
        msg.attach(image)
        img_data = open(imgurl2, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(imgurl2))
        msg.attach(image)

        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login("mail", "password")
        mailserver.sendmail("mail", "mail", msg.as_string())
        mailserver.quit()
        print(time.strftime("%H:%M:%S") + " données envoyé !")
    time.sleep(300)

