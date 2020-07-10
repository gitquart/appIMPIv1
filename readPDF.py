#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 16:41:05 2020
@author: ulysesrico
-This program converts from PDF to txt file
"""


# importing required modules 
import PyPDF2 
import os
import writeFile

dirGacetaPDF='/Users/ulysesrico/RespaldoMacUly/quart/Gaceta10epocaPDF/'
dirGacetaTxt='/Users/ulysesrico/RespaldoMacUly/quart/Gaceta10epocaTxt/'


#PDF pages are 0-based
for file in os.listdir(dirGacetaPDF):
    if file.endswith(".pdf") or file.endswith(".PDF"):
        
        pdfFileObj = open(dirGacetaPDF+file, 'rb') 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        if pdfReader.isEncrypted:
            pdfReader.decrypt('')
            
        #Get total number of pages
        nPages=pdfReader.numPages   
        i=0
        while i < nPages:
            
            pageObj = pdfReader.getPage(i) 
            pageContent=pageObj.extractText()
                 
            #Get the filename without extension
            fileName=os.path.splitext(file)[0]
            #Create a File .txt
            appendInfoToFile(dirGacetaTxt,fileName+".txt",pageContent)
            i=i+1
                
        pdfFileObj.close() 
        print("Terminó :",file)
print("¡PROCESO TERMINADO!")        
        
