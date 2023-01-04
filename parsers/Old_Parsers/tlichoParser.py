# nltk data available at C:\Users\marcs\AppData\Roaming\nltk_data

#Tlicho Agreement ATRIS Parser
#Marc St. Pierre 1/3/2023

import string
import csv
import requests
from bs4 import BeautifulSoup

url = requests.get('https://www.rcaanc-cirnac.gc.ca/eng/1292948193972/1543262085000')
soup = BeautifulSoup(url.content, 'html.parser')
dbtitle = 'TLprovisionsdb.csv'
agreement = 'Tlicho Agreement'
year = '2003'
part = ''  # for style purposes this cannot be called a 'chapter'
section = ''  # refers to any subheading under a part heading
roman = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
alpha = list(string.ascii_lowercase)
prevEnumType = 'lst-spcd'
startflag = 0
intIndex = 0
alphaIndex = 0
romanIndex = 0
provNum = 0
data = []

for child in soup.h1.next_elements:
    if child.name == 'h2':
        part = child.get_text()
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
            data.append([provNum, part, section, child.get_text()])
        except ValueError:
            data.append([provNum, part, section, child.get_text()])
        except IndexError:
            data.append([provNum, part, section, child.get_text()])
    if child.name == 'li':
        if 'class' in child.parent.attrs:
            if 'lst-upr-alph' in child.parent.attrs['class'][0]:
                enumType = 'lst-lwr-alph'
            else:
                enumType = child.parent.attrs['class'][0]
                
        if 'start' in child.parent.attrs and startflag == 0:
            intIndex = int(child.parent.attrs['start'][0]) - 1
            startflag = 1
            
        if enumType == 'lst-spcd' and prevEnumType == 'lst-spcd':
            intIndex += 1
            data.append([str(provNum) + '(' + str(intIndex) + ')', part, section, child.get_text()])
        elif 'lst-lwr-alph' in enumType and prevEnumType == 'lst-spcd':
            alphaIndex = 0
            data.append([str(provNum) + '(' + alpha[alphaIndex] + ')', part, section, child.get_text()])
        elif 'lst-lwr-alph' in enumType and 'lst-lwr-alph' in prevEnumType:
            alphaIndex += 1
            data.append([str(provNum) + '(' + alpha[alphaIndex] + ')', part, section, child.get_text()])
        elif 'lst-lwr-rmn' in enumType and 'lst-lwr-alph' in prevEnumType:
            romanIndex = 0
            data.append([str(provNum) + '(' + alpha[alphaIndex] + ')' + '(' + roman[romanIndex] + ')', part, section, child.get_text()])
        elif 'lst-lwr-rmn' in enumType and 'lst-lwr-rmn' in prevEnumType:
            romanIndex += 1
            data.append([str(provNum) + '(' + alpha[alphaIndex] + ')' + '(' + roman[romanIndex] + ')', part, section, child.get_text()])
        elif 'lst-lwr-alph' in enumType and 'lst-lwr-rmn' in prevEnumType:
            alphaIndex += 1
            data.append([str(provNum) + '(' + alpha[alphaIndex] + ')', part, section, child.get_text()])
        elif enumType == 'lst-spcd' and 'lst-lwr-alpha' in prevEnumType:
            intIndex += 1
            data.append([str(provNum) + '(' + str(intIndex) + ')', part, section, child.get_text()])
        elif enumType == 'lst-spcd' and 'lst-lwr-rmn' in prevEnumType:
            intIndex += 1
            data.append([str(provNum) + '(' + str(intIndex) + ')', part, section, child.get_text()])
        else:
            data.append([provNum, part, section, child.get_text()])
        prevEnumType = enumType

with open(dbtitle, 'w', newline='') as csvfile:
    provisionswriter = csv.writer(csvfile)
    provisionswriter.writerow(['agreement', 'year', 'provisionNum', 'part', 'section', 'provisionText'])
    for i in data:
        row = [agreement, year] + i
        provisionswriter.writerow(row)
    csvfile.close()


# for i in range(100):
#     print(data[i])

# for i in data:
#     print(i)



