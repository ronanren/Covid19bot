# -*- coding: UTF-8 -*-
import requests
import re


p = requests.get('https://www.worldometers.info/coronavirus/')

indexFrance = p.text.find(
    '<a class="mt_a" href="country/france/">France</a>')
indexFranceEnd = indexFrance + p.text[indexFrance:].find("</tr>")

PlaceInWorld = p.text[:indexFranceEnd].count('href="country/') + 1

cases = re.findall(r'[\d]{1,3},[\d]{3}|\d{3}', str(
    p.text[indexFrance:indexFranceEnd]))
data = ["Total Cases", "New Cases", "Total Deaths",
        "New Deaths", "Total Recovered", "Active Cases", "Critical"]

print("Nous sommes " + str(PlaceInWorld) + "ème dans le monde")
for i in range(0, 7):
    print(data[i] + ": " + cases[i])
