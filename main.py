# -*- coding: UTF-8 -*-
import requests
import re
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import csv

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
            tabNewCases.append(row[2].replace(".", ""))
            tabTotalDeaths.append(row[3].replace(".", ""))
            tabNewDeaths.append(row[4].replace(".", ""))
            tabTotalRecovered.append(row[5].replace(".", ""))
            tabActiveCases.append(row[6].replace(".", ""))
            tabCritical.append(row[7].replace(".", ""))
            tabDate.append(line_count)
            line_count += 1
        else:
            line_count += 1
print(tabDate)
print(tabTotalCases)
plt.plot(tabDate, tabTotalCases, "o-",
         label="Population malade", linewidth=3)
plt.axis([0, numberOfDay, 0, ceil((int(cases[0].replace(".", ""))/5000))*5000])
plt.legend()
plt.grid(True)

plt.show()
