"""
Quart: This program is a 'Demo' that will read patents and store them in a spreadsheet

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import time
import requests 
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

chromedriver_autoinstaller.install()
download_dir='C:\\Users\\Acer\\Downloads'
#Set options for chrome
options = Options()
profile = {
           "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
           "download.default_directory": download_dir , 
           "download.extensions_to_open": "applications/pdf",
           "plugins.always_open_pdf_externally": True
           }

options.add_experimental_option("prefs", profile)

browser=webdriver.Chrome(chrome_options=options)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
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
        time.sleep(2)
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
                        #Id of the input for each row index 0
                        #MainContent_gdDoctosExpediente_ImageButton1_0 
                        btn=t.findChildren('input',recursive=True)
                        if btn:
                            chunks=str(btn[0]).split(' ')
                            #Getting ID alone
                            parts=chunks[2].split('=')
                            val_name=parts[1] 
                            javaScript = "document.getElementsByName("+val_name+")[0].click();"
                            browser.execute_script(javaScript)
                            time.sleep(1)
                            pdf_source=''
                            pdf_source = browser.find_element_by_tag_name('iframe').get_attribute("src")
                            if pdf_source!='':
                                #Get the url of the source
                                time.sleep(1)
                                browser.get(pdf_source)
                                #Finf the href with innerText 'aquí'
                                link=browser.find_element_by_tag_name('a')
                                if link.text=='aquí':
                                    link.click()
                                    #Wait 10 seconds for download
                                    time.sleep(10)
                                
                        else:
                            print(t.text)
                    countRow=countRow+1
                    if countRow==1:
                        break 
        if countRow==1:
            break        
        
browser.quit()    
        
   