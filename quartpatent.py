"""
Quart: This program is a 'Demo' that will read patents and store them in a spreadsheet

"""

from selenium import webdriver
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import time
import requests 

chromedriver_autoinstaller.install()
browser=webdriver.Chrome()

url="https://vidoc.impi.gob.mx/DocVidoc?param=UArQD03r3Uh6mcI3WYBduaA5g1uEGDCi"
response= requests.get(url)
status= response.status_code
StartID=13000
EndID=14000
count=0

if status==200:
    for i in range(StartID,EndID):
        #File as "Expediente"
        urlFile="https://vidoc.impi.gob.mx/visor?usr=SIGA&texp=SI&tdoc=E&id=MX/a/2015/0"+str(i)
        browser.get(urlFile)
        time.sleep(1)
        file_html = BeautifulSoup(browser.page_source, 'lxml')
        table=file_html.find('table')
        if table is not None:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                print(row)
        count=count+1
        if count==1:
            break 
        
    browser.quit()    
        
   