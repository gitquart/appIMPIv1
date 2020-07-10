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
import writeFile as wf


def readPdf(fileWithPath,extensionToConvert):
    #PDF pages are 0-based
    if fileWithPath.endswith(".pdf") or fileWithPath.endswith(".PDF"):
        pdfFileObj = open(fileWithPath, 'rb') 
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
            wf.appendInfoToFile(dirGacetaTxt,fileName+"."+extensionToConvert,pageContent)
            i=i+1
        
        pdfFileObj.close() 
        return true
        
        
        
      
        
