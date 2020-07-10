"""
Quart: This program is a 'Demo' that will read patents and store them in a spreadsheet

"""

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import time
import requests 
from selenium.webdriver.chrome.options import Options
import xlwt 
from xlwt import Workbook


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

browser=webdriver.Chrome(options=options)
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
            #The complete table if exists
            table_rows = table.findAll('tr')
            #Iterate all the rows in the table
            for tr in table_rows:
                #Every <td> has one element only
                txt_number=''
                txt_barcode=''
                txt_document=''
                txt_desc=''
                txt_type=''
                txt_date=''
                pdf_name=''
                pdf_file_name=''
                if tr.nextSibling!='\n':
                    td = tr.findAll('td')
                    fieldPosition=0
                    for t in td:
                        fieldPosition=fieldPosition+1
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
                            #Get the name of the pdf document
                            time.sleep(2) #Time sleep to give time to read the 'modal-text'
                            pdf_name=browser.find_element_by_class_name('modal-title').text
                            time.sleep(1)
                            pdf_name=str(pdf_name).strip()
                            pdf_file_name=pdf_name.replace('/','_')
                            pdf_source=''
                            pdf_source = browser.find_element_by_tag_name('iframe').get_attribute("src")
                            time.sleep(2)
                            if pdf_source!='':
                                #Get the url of the source
                                browser.get(pdf_source)
                                time.sleep(2)
                                #Finf the href with innerText 'aquí'
                                link=browser.find_element_by_tag_name('a')
                                time.sleep(1)
                                if link.text=='aquí':
                                    link.click()
                                    #Wait 'X' seconds for download
                                    time.sleep(20)      
                        else:
                            """
                            Structure of <tr/>:
                            Number (1),BarCode (2),Document (3),Description (4),Type (5),Date (6),PDF (7)
                            """  
                            if fieldPosition==1:
                                txt_number=t.text
                                continue
                            if fieldPosition==2:
                                txt_barcode=t.text
                                continue
                            if fieldPosition==3:
                                txt_document=t.text
                                continue 
                            if fieldPosition==4:
                                txt_desc=t.text
                                continue
                            if fieldPosition==5:
                                txt_type=t.text
                                continue  
                            if fieldPosition==6:
                                txt_date=t.text 
                                continue            
                    #End of loop of every td in a single row 
                    #Excel process
                     
                    print('pdf name:',pdf_name)  
                    print('pdf_file',pdf_file_name)
                    print('number: ',txt_number)
                    print('barcode:',txt_barcode)
                    print('document:',txt_document)
                    print('desc:',txt_desc)
                    print('type:',txt_type)
                    print('date:',txt_date)
                      
                    countRow=countRow+1
                    if countRow==1:
                        break
            #End of row loop         
        if countRow==1:
            break        
        
browser.quit() 

    
       
        
   