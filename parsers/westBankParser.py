# nltk data available at C:\Users\marcs\AppData\Roaming\nltk_data

# Westbank Self Government Agreement ATRIS Parser
# Marc St. Pierre 1/3/2023

import string
import csv
import requests
from bs4 import BeautifulSoup

url = requests.get('https://www.rcaanc-cirnac.gc.ca/eng/1100100031766/1543001371378')
soup = BeautifulSoup(url.content, 'html.parser')
dbtitle = 'WBprovisionsdb.csv'
agreement = 'Westbank First Nation Self Government Agreement'
year = '2003'
part = ''
section = ''
roman = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
alpha = list(string.ascii_lowercase)
prevEnumType = 'lst-spcd'
alphaIndex = 0
romanIndex = 0
provNum = 0
data = []

for child in soup.h1.next_elements:
    if child.name == 'h2':
        part = child.get_text()
        section = ''
        startflag = 0
    if child.name in ['h3', 'h4', 'h5', 'h6']:
        section = child.get_text()
        startflag = 0
    if child.name == 'p':
        alphaIndex = 0
        romanIndex = 0
        intIndex = 0
        startflag = 0
        prevEnumType = 'lst-spcd'
        try:
            int(child.get_text()[0])
            provNum = (child.get_text().split(' ', 1)[0]).strip('\n')
            text = " ".join(child.get_text().split(' ')[1:])
            data.append([provNum, part, section, text])
        except ValueError:
            data.append([provNum, part, section, child.get_text()])
        except IndexError:
            data.append([provNum, part, section, child.get_text()])
    if child.name == 'li':
        if 'class' in child.parent.attrs:
            enumType = child.parent.attrs['class'][0]
        if enumType == 'lst-spcd' and prevEnumType == 'lst-spcd':
            provNum += 1
            data.append([str(provNum), part, section, child.get_text()])
        elif enumType == 'lst-lwr-alph' and prevEnumType == 'lst-spcd':
            alphaIndex = 0
            data.append([str(provNum) + "(" + alpha[alphaIndex] + ")", part, section, child.get_text()])
        elif enumType == 'lst-lwr-alph' and prevEnumType == 'lst-lwr-alph':
            alphaIndex += 1
            data.append([str(provNum) + "(" + alpha[alphaIndex] + ")", part, section, child.get_text()])
        elif enumType == 'lst-lwr-rmn' and prevEnumType == 'lst-lwr-alph':
            romanIndex = 0
            data.append([str(provNum) + "(" + alpha[alphaIndex] + ")" + "(" + roman[romanIndex] + ")", part, section, child.get_text()])
        elif enumType == 'lst-lwr-rmn' and prevEnumType == 'lst-lwr-rmn':
            romanIndex += 1
            data.append([str(provNum) + "(" + alpha[alphaIndex] + ")" + "(" + roman[romanIndex] + ")", part, section, child.get_text()])
        elif enumType == 'lst-lwr-alph' and prevEnumType == 'lst-lwr-rmn':
            alphaIndex += 1
            data.append([str(provNum) + "(" + alpha[alphaIndex]+ ")", part, section, child.get_text()])
        elif enumType == 'lst-spcd' and prevEnumType == 'lst-lwr-alph':
            provNum += 1
            data.append([str(provNum), part, section, child.get_text()])
        elif enumType == 'lst-spcd' and prevEnumType == 'lst-lwr-rmn':
            provNum += 1
            data.append([str(provNum), part, section,  child.get_text()])
        else:
            data.append([0, part, section,  child.get_text()])
        prevEnumType = enumType

with open(dbtitle, 'w', newline='') as csvfile:
    provisionswriter = csv.writer(csvfile)
    provisionswriter.writerow(['agreement', 'year', 'provisionNum', 'part', 'section', 'provisionText'])
    for i in data:
        row = [agreement, year] + i
        provisionswriter.writerow(row)
    csvfile.close()


for i in range(100):
    print(data[i])

# for i in data:
#     print(i)



