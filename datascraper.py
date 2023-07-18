#Importing Libraries
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse ,urljoin
# from urllib.request import urlparse, urljoin
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


#Starting our browser instance
driver_path = r"programs ( 1 )\chromedriver.exe"
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
option.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=driver_path, options=option)

#We are setting the arrays
main_location = []
sub_location = []
hood = []
size= []
pricepm = []
frontage = []
purpose = []
street_width = []

#Setting an absolute html variable
aqar = 'https://sa.aqar.fm/'

#Script 
for i in range(32, 64): #going through each page
    try:
        driver.get(r'https://sa.aqar.fm/%D8%A3%D8%B1%D8%A7%D8%B6%D9%8A-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/' + f'{i}')
    except:
        break 
    sleep(2)

    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')

    res = soup.find_all('h4', class_='listingCard_title__45XgY')
    links = []
    for result in res:  
        link = result.find('a');
        links.append(link)
       
    iter = 0
    for link in links: #getting the links to each land
        iter = iter +1
        http = urljoin(aqar, link.get('href')) #merging the links
        driver.get(http)
        sleep(2)

        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        tree= soup.find_all('li', class_='breadcrumb-module_item__ZLYPz') # Getting the location
        
        if(len(tree) <=3):
            continue

        if len(tree) > 4:
            main_location.append(tree[2].text)
            sub_location.append(tree[3].text)
            hood.append(tree[4].text)
        else:
            main_location.append(tree[2].text)
            sub_location.append(np.nan)
            hood.append(tree[3].text)        
        #Getting the size, price, purpose, and frontage
        table = soup.find_all('div', class_='SpecsCard-module_label__e7FSF')

        index = 0  
        frontB = purposeB = streetB = sizeB = priceB = False
        for label in table:
            front = soup.find_all('div', class_='SpecsCard-module_value__7U7rW')
            if(label.text == 'الواجهة'):
                frontB = True
                frontage.append(front[index].text)
            elif(label.text == 'الغرض'):
                purposeB = True
                purpose.append(front[index].text)
            elif(label.text == 'عرض الشارع'):
                streetB = True
                numberFilter = front[index].text[:-1].replace(',','')
                street_width.append(numberFilter)
            elif(label.text == 'المساحة'):
                sizeB = True
                numberFilter = front[index].text[:-2].replace(',','')
                size.append(numberFilter)
            elif(label.text == 'سعر المتر'):
                priceB = True
                numberFilter = front[index].text[:-4].replace(',','')
                pricepm.append(numberFilter)
            index = index + 1;    

        if(frontB == False):
            frontage.append(np.nan)
        if(purposeB == False):
            purpose.append(np.nan)
        if(streetB == False):
            street_width.append(np.nan)
        if(sizeB == False):
            size.append(np.nan)
        if(priceB == False):
            pricepm.append(np.nan)
       
        
       

            

#Creating our df

df = pd.DataFrame({
    'mainlocation' : main_location,
    'sublocation' : sub_location,
    'neighborhood' : hood,
    'frontage' : frontage,
    'purpose' : purpose,
    'streetwidth' : street_width,
    'size' : size,
    'Pricepm' : pricepm
})
df.to_csv('newDataset.csv',mode='a',index=False) # Saving the data in a csv


