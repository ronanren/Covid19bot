import requests
import re


p = requests.get('https://www.worldometers.info/coronavirus/')

indexFrance = p.text.find(
    '<a class="mt_a" href="country/france/">France</a>')
indexFranceEnd = indexFrance + p.text[indexFrance:].find("</tr>")

cases = re.findall(r'[\d]{1,3},[\d]{3}|\d{3}', str(
    p.text[indexFrance:indexFranceEnd]))

print('cas en 24h : ' + cases[3])
