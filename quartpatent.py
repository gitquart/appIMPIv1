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
import os


chromedriver_autoinstaller.install()
download_dir='C:\\Users\\Acer\\Downloads\\'
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


for i in range(StartID,EndID):
    #This iteration gets each file
    urlExp="https://vidoc.impi.gob.mx/visor?usr=SIGA&texp=SI&tdoc=E&id=MX/a/2015/0"+str(i)
    response= requests.get(urlExp)
    status= response.status_code
    if status==200:
        browser.get(urlExp)
        time.sleep(1)
        path=''
        expedient_name=''
        exp_html=''
        table=''
        exp_html = BeautifulSoup(browser.page_source, 'lxml')
        table=exp_html.find('table')
        expedient_name=exp_html.find('h3').text
        expedient_name=expedient_name.replace(' ','_')  
        expedient_name=expedient_name.replace('/','_') 
        path=download_dir+expedient_name+'.xlsx'
        res=os.path.isfile(path)
        if res==False:
            if table is not None:
                #The complete table if exists
                table_rows = table.findAll('tr')
                #Iterate all the rows in the table
                countRow=0
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
                                pdf_name=txt_document.replace('/','_')
                                pdf_file_name=pdf_name.replace('/','_')
                                pdf_file_name=pdf_file_name+'.pdf'
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
                        wb = Workbook()  
                        sheet1 = wb.add_sheet('Patents') 
                        #Write(row,column)
                        #Headers
                        sheet1.write(0, 0, 'Number') 
                        sheet1.write(0,1,'Bar code')
                        sheet1.write(0,2,'Document')
                        sheet1.write(0,3, 'Description') 
                        sheet1.write(0,4,'Type')
                        sheet1.write(0,5,'Date')
                        sheet1.write(0,6,'Pdf file')
                    
                        #Row
                        countRow=countRow+1
                        sheet1.write(countRow,0,txt_number)
                        sheet1.write(countRow,1,txt_barcode)
                        sheet1.write(countRow,2,txt_document)
                        sheet1.write(countRow,3,txt_desc)
                        sheet1.write(countRow,4,txt_type)
                        sheet1.write(countRow,5,txt_date)
                        sheet1.write(countRow,6,pdf_file_name)
                     
                                    
                        wb.save(download_dir+expedient_name+'.xlsx') 
                     
                   
                        if countRow==1:
                            break
                #End of row loop         
            if countRow==1:
                break        
        
browser.quit() 

    
       
        
   