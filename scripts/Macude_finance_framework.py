#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

# Read data frame containing General Infomation of the courses
df = pd.read_excel('FinanceUniversityData.xlsx', sheet_name = 'UniversityData')
Crname = df['Course Name'].values
Cwebsite = df['Course Website'].values
tag = df['Tag'].values
clname = df['Class Name'].values

# Read finance program's specific info
financeTerm = pd.read_excel('FinanceUniversityData.xlsx', sheet_name = 'FinanceData')
financeLevel = financeTerm['Degree Level'].values
financeTheme = financeTerm['Course Themes'].values
financeTopic = financeTerm['Digital Topics'].values
financeLanguage = financeTerm['Programming Language'].values

def keywordSearch(keyword:list, content:list):
    found=[]
    flag=0
    for each in keyword:
        if str(each).lower() in content:
            found.append(each.lower())
            flag=1
    return flag, found
    
levelFound=[]
themeFound=[]
topicFound=[]
languageFound=[]

contents=[]
#Store Course curriculum
termsCount=[]
    
for i in range(len(Crname)):
    pageLink = Cwebsite[i]
    response = requests.get(pageLink, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',})
    html = response.content  # get the html
    time.sleep(2)  # wait 2 secs
    soup = BeautifulSoup(html.decode('ascii', 'ignore'), 'lxml')  # parse the html
    reviews = soup.findAll(tag[i], {'class': clname[i]})  # get all the review divs
    for review in reviews:
        content = review.text.lower()
        contents.append(content)

    flag,found = keywordSearch(financeLevel, content)
    if flag ==1:
        levelFound.append(found)
    if flag!=1:
        levelFound.append('No Finance Level Info Found')       
            
    flag,found = keywordSearch(financeTheme, content)
    if flag ==1:
        themeFound.append(found)
    if flag!=1:
        themeFound.append('No Finance Theme Info Found')       
            
    flag,found = keywordSearch(financeTopic, content)
    if flag ==1:
        topicFound.append(found)
    if flag!=1:
        topicFound.append('No Finance Topic Info Found')       
            
    flag,found = keywordSearch(financeLanguage, content)
    if flag ==1:
        languageFound.append(found)
    if flag!=1:
        languageFound.append('No Finance Language Info Found')       

        
newdf= df
newdf = newdf.drop(['Tag', 'Class Name'], axis=1)

newdf['Course Curriculum']= contents
newdf['Degree Level']=levelFound
newdf['Course Themes']=themeFound
newdf['Digital Topics']=topicFound
newdf['Programming Language']=languageFound

newdf.head()

newdf.to_excel('Macude_finance_scrapped.xlsx', header=True, index= False)
