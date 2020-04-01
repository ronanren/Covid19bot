# -*- coding: UTF-8 -*-
import requests
import re
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import csv
import locale

# Mettre les dates en francais
locale.setlocale(locale.LC_TIME, '')

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

'''
f = open("data/dataFrance.csv", "a+")
f.write(str(date.today()) + "," + cases[0] + "," + cases[1] +
        "," + cases[2] + "," + cases[3] + "," + cases[4] + "," + cases[5] + "," + cases[5] + "," + str(PlaceInWorld) + "\n")
f.close()
'''
# Text data of day
print("Nous sommes " + str(PlaceInWorld) + "ème dans le monde")
for i in range(0, 7):
    try:
        print(data[i] + ": " + cases[i])
    except:
        print("erreur")

# Graphic of day

tabTotalCases = []
tabNewCases = []
tabTotalDeaths = []
tabNewDeaths = []
tabTotalRecovered = []
tabActiveCases = []
tabCritical = []
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
            tabDate.append(line_count)
            line_count += 1
        else:
            line_count += 1


# Graphique 1
plt.plot(tabDate, tabTotalCases, "o-",
         label="Population malade", linewidth=3, color="#9b59b6")
plt.plot(tabDate, tabActiveCases, "o-",
         label="Population active", linewidth=3, color="#f1c40f")
plt.plot(tabDate, tabTotalRecovered, "o-",
         label="Population guérie", linewidth=3, color="#2ecc71")
plt.plot(tabDate, tabCritical, "o-",
         label="Population critique", linewidth=3, color="#e74c3c")
plt.plot(tabDate, tabTotalDeaths, "o-",
         label="Population décédée", linewidth=3, color="#2c3e50")


plt.axis([0, numberOfDay, 0, ceil(
    (int(cases[0].replace(".", ""))/5000))*5000])
plt.legend(loc='upper left')
plt.grid(True)
plt.xlabel('Jours à partir du 17 mars 2020')
plt.ylabel('Population')
plt.title('Avancé du COVID-19 en France du ' +
          str(date.today().strftime("%A %d %B %Y")))
plt.show()
# plt.savefig('data/' + str(date.today()) + '.png')

# Graphique 2
plt.plot(tabDate, tabNewCases, "o-",
         label="Population touchée aujourd'hui", linewidth=3, color="#9b59b6")
plt.plot(tabDate, tabNewDeaths, "o-",
         label="Population décédée aujourd'hui", linewidth=3, color="#2c3e50")

# plt.axis([0, numberOfDay, 0, ceil((int(cases[1].replace(".", ""))/1000))*1000])
plt.axis([0, numberOfDay, 0, ceil(7500/1000)*1000])

plt.legend(loc='upper left')
plt.grid(True)
plt.xlabel('Jours à partir du 17 mars 2020')
plt.ylabel('Population')
plt.title('Avancé du COVID-19 en France du ' +
          str(date.today().strftime("%A %d %B %Y")))
plt.show()
