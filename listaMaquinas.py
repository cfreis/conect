#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:17:29 2019

@author: clovis
"""

import requests
import lxml.html as lh
import pandas as pd
from unicodedata import normalize
codif='utf-8'

def ordenaIp(ipAnt):
    #coloca os ips na ordem Interno, Externo e URL se existirem
    ipNew=['','','']
    idx=1
    for idx in range(0,len(ipAnt)):
        if ipAnt[idx][0:3] == '10.':
            ipNew[0]=ipAnt[idx]
        elif ipAnt[idx][0:3] == '177':
            ipNew[1]=ipAnt[idx]
        else :
            ipNew[2]=ipAnt[idx]
    return(ipNew)            


url = 'http://ucrania.imd.ufrn.br/mediawiki/index.php/Lista_de_M%C3%A1quinas' #Create a handle, page, to handle the contents of the website
page = requests.get(url)#Store the contents of the website under doc
doc = lh.fromstring(page.content)#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')

#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]

tr_elements = doc.xpath('//tr')#Create empty list
col=[]
i=0#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    name=normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    name=name.split(" ")[0]
    name=name.replace("\n","")
    print('%d:"%s"'%(i,name))
    col.append((name,[]))
    
j=1
#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 10, the //tr data is not from our table 
    if len(T)!=9:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content()
        data=data.replace("\n","")
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column 
        i+=1

[len(C) for (title,C) in col]

Dict={title:column for (title,column) in col}
Dict["Nome"]
Dict.keys()
df=pd.DataFrame(Dict)        

lins=df.shape[0]
cols=df.shape[1]
lin=1
ipExt=[]
ipInt=[]
ipUrl=[]
for lin in range(0,lins):
    #pega o primeiro elemento da coluna ip da linha 
    ip=df.iloc[lin][["Ip"]][0].replace(" ","")
    ip=ip.split("/")
    ip=ordenaIp(ip)    
    ipInt.append(ip[0])
    ipExt.append(ip[1])
    ipUrl.append(ip[2])

#Acrescenta as novas colunas no df
df['ipInt']=ipInt
df['ipExt']=ipExt
df['ipUrl']=ipUrl
df.drop(["Ip"], axis = 1, inplace = True) 


