
# coding: utf-8

# In[206]:

import re
import requests
import csv
import os
from datetime import datetime
from bs4 import BeautifulSoup

#TOMAMOS LA URL
url = 'https://www.iguanasell.es/collections/montegrappa-escritura-game-of-thrones-subcat.html'
resp = requests.get(url)

#DEFINIMOS LOS CAMPOS QUE VAMOS A EXTRAER DE LA URL
FIELDS = ('price','priceCurrency','seller','availability','itemCondition')
class Elemento(object):
    name = "",
    price = 0,  
    priceCurrency = "",
    seller = "",
    availability = "",
    itemCondition = ""

#HACEMOS USO DE LA LIBRERÍA BEAUTIFULSOUP PARA TRABAJAR CON EL CÓDIGO FUENTE DE LA URL.    
soup = BeautifulSoup(resp.text, 'html.parser')

#RASTREAMOS EL CÓDIGO PARA OBTENER LOS DATOS QUE QUEREMOS, CUANDO LOS TENEMOS, LOS METEMOS EN UN OBJETO, Y ESTE EN UN ARRAY
articulos = []
for row in soup.find_all('div', attrs={'class':'product-details'}):
    objeto = Elemento()
    objeto.name = row.find('span', attrs={'class':'title'}).text.replace(',',';')
    
    for field in FIELDS:
        setattr(objeto, field, row.find('meta', attrs={'itemprop':field})['content'])

    articulos.append(objeto)


#DEFINIMOS EL FICHERO, SINO EXISTE, SE CREA Y ADEMÁS SE AÑADEN LAS CABECERAS.    
fichero = "IguanaSell_GOT_dataset.csv"
header = []
try:
    open(fichero, 'r')
except IOError:
    open(fichero, 'w')
    header = ["Date", "Time","Name","Price", "PriceCurrency","Seller", "Availability", "ItemCondition"]
    
#OBTENEMOS FECHA Y HORA PARA AÑADIRLO A NUESTRO CONJUNTO DE DATOS.
now = datetime.now()
strDate = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
strTime = str(now.hour)+":"+str(now.minute)

#AÑADIMOS CADA OBJETO COMO UN REGISTRO NUEVO DEL FICHERO.
with open(fichero, 'a', newline='') as csvFile:
    writer = csv.writer(csvFile)
    if (len(header) > 0):
        writer.writerow(header)
    for item in articulos:
        writer.writerow([strDate,strTime,item.name, item.price.replace(',',''), item.priceCurrency, item.seller, item.availability, item.itemCondition])




# In[ ]:



