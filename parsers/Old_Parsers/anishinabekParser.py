# nltk data available at C:\Users\marcs\AppData\Roaming\nltk_data

#Anishinabek Nation Governance Agreement ATRIS Parser
#Marc St. Pierre 12/21/2022

import string
import csv
import requests
from bs4 import BeautifulSoup

url = requests.get('https://www.rcaanc-cirnac.gc.ca/eng/1663876084479/1663876161241')
soup = BeautifulSoup(url.content, 'html.parser')
dbtitle = 'ANprovisionsdb.csv'
agreement = 'Anishinabek Nation Governance Agreement'
year = '2019'
topic = ''
alpha = list(string.ascii_lowercase)
alphaIndex = 0
provNum = 0
data = []

for child in soup.h1.next_elements:
    if child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        topic = child.get_text()
    if child.name == 'p':
        alphaIndex = 0
        prevEnumType = 'lst-spcd'
        try:
            float(child.get_text().split(' ', 1)[0])
            provNum = child.get_text().split(' ', 1)[0]
            data.append([provNum, topic, child.get_text()])
        except ValueError:
            data.append([provNum, topic, child.get_text()])
    if child.name == 'li':
        if 'class' in child.parent.attrs:
            enumType = child.parent.attrs['class'][0]
            if enumType == 'lst-lwr-alph':
                data.append([str(provNum) + alpha[alphaIndex], topic, child.get_text()])
                alphaIndex += 1
        else:
            data.append([provNum, topic, child.get_text()])

with open(dbtitle, 'w', newline='') as csvfile:
    provisionswriter = csv.writer(csvfile)
    provisionswriter.writerow(['agreement', 'year', 'provisionNum', 'topic', 'provisionText'])
    for i in data:
        row = [agreement, year] + i
        provisionswriter.writerow(row)
    csvfile.close()


# for i in range(300):
#     print(data[i])

# for i in data:
#     print(i)



