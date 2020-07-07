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
#url="https://vidoc.impi.gob.mx/DocVidoc?param=UArQD03r3Uh6mcI3WYBduaA5g1uEGDCi"
StartID=13000
EndID=14000
countRow=0

for i in range(StartID,EndID):
    #File as "Expediente"
    #This iteration gets each file
    urlFile="https://vidoc.impi.gob.mx/visor?usr=SIGA&texp=SI&tdoc=E&id=MX/a/2015/0"+str(i)
    response= requests.get(urlFile)
    status= response.status_code
    if status==200:
        browser.get(urlFile)
        time.sleep(1)
        file_html = BeautifulSoup(browser.page_source, 'lxml')
        table=file_html.find('table')
        if table is not None:
            """
            Structure of <tr/>:
            Number (1),BarCode (2),Document (3),Description (4),Type (5),Date (6),PDF (7)
            """
            #The complete table if exists
            table_rows = table.findAll('tr')
            #Iterate all the rowd in the table
            for tr in table_rows:
                #For this code every <td> has one element only
                if tr.nextSibling!='\n':
                    td = tr.findAll('td')
                    for t in td:
                        btn=t.findChildren('input',recursive=True)
                        if btn:
                            print('Hay input')    
                        else:
                            print(t.text)
                    countRow=countRow+1
                    if countRow==1:
                        break 
        if countRow==1:
            break        
        
browser.quit()    
        
   