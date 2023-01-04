# nltk data available at C:\Users\marcs\AppData\Roaming\nltk_data

#Tsawwassen Nation Final Agreement ATRIS Parser
#Marc St. Pierre 12/22/2022

import string
import csv
import requests
from bs4 import BeautifulSoup

url = requests.get('https://www.rcaanc-cirnac.gc.ca/eng/1100100022706/1617737111330')
soup = BeautifulSoup(url.content, 'html.parser')
dbtitle = 'TSprovisionsdb.csv'
agreement = 'Tsawwassen First Nation Final Agreement'
year = '2007'
topic = ''
alpha = list(string.ascii_lowercase)
roman = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
prevEnumType = 'lst-spcd'
alphaIndex = 0
romanIndex = 0
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
            provNum = (child.get_text().split(' ', 1)[0]).strip('\n')
            data.append([provNum, topic, child.get_text()])
        except ValueError:
            data.append([provNum, topic, child.get_text()])
    if child.name == 'li':
        if 'class' in child.parent.attrs:
            enumType = child.parent.attrs['class'][0]
            if enumType == 'lst-upr-alph':
                enumType = 'lst-lwr-alph'
        if enumType == 'lst-spcd' and prevEnumType == 'lst-spcd':
            provNum += 1
            data.append([str(provNum), topic, child.get_text()])
        elif enumType == 'lst-lwr-alph' and prevEnumType == 'lst-spcd':
            alphaIndex = 0
            data.append([str(provNum) + alpha[alphaIndex], topic, child.get_text()])
        elif enumType == 'lst-lwr-alph' and prevEnumType == 'lst-lwr-alph':
            alphaIndex += 1
            data.append([str(provNum) + alpha[alphaIndex], topic, child.get_text()])
        elif enumType == 'lst-lwr-rmn' and prevEnumType == 'lst-lwr-alph':
            romanIndex = 0
            data.append([str(provNum) + alpha[alphaIndex] + roman[romanIndex], topic, child.get_text()])
        elif enumType == 'lst-lwr-rmn' and prevEnumType == 'lst-lwr-rmn':
            romanIndex += 1
            data.append([str(provNum) + alpha[alphaIndex] + roman[romanIndex], topic, child.get_text()])
        elif enumType == 'lst-lwr-alph' and prevEnumType == 'lst-lwr-rmn':
            alphaIndex += 1
            data.append([str(provNum) + alpha[alphaIndex], topic, child.get_text()])
        elif enumType == 'lst-spcd' and prevEnumType == 'lst-lwr-alph':
            provNum += 1
            data.append([str(provNum), topic, child.get_text()])
        elif enumType == 'lst-spcd' and prevEnumType == 'lst-lwr-rmn':
            provNum += 1
            data.append([str(provNum), topic, child.get_text()])
        else:
            data.append([provNum, topic, child.get_text()])
        prevEnumType = enumType

with open(dbtitle, 'w', newline='') as csvfile:
    provisionswriter = csv.writer(csvfile)
    provisionswriter.writerow(['agreement', 'year', 'provisionNum', 'topic', 'provisionText'])
    for i in data:
        row = [agreement, year] + i
        provisionswriter.writerow(row)
    csvfile.close()


# for i in range(100):
#     print(data[i])

# for i in data:
#     print(i)



