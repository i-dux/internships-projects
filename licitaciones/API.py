#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pandas as pd


# Se puede obtener el listado completo de licitaciones aquí: https://desarrolladores.mercadopublico.cl/OCDS/Listado

# # Palabras claves

# In[29]:


def palabras_claves():     
    palabras_claves = []
    seguir = True
    while seguir:
        print('Escribe palabra clave o apreta 0 para terminar')
        palabra = input()
        if palabra != '0':
            palabras_claves.append(palabra)
        else:
            seguir = False

    palabras = []        

    for elemento in palabras_claves:
        ele = elemento.upper()
        palabras.append(ele)
    return palabras


# In[30]:


def tiene_claves(palabras, descripcion):     
    descripcion = descripcion.upper()
    
    if len(palabras) == 0:
        return False
    
    for elemento in palabras:
        if elemento in descripcion:
            return True
    else:
        return False


# # Hacer la consulta por año y mes

# In[60]:


print('Escriba el año')
año = input()
print('Escriba el mes como número del 1 al 12')
mes = input()

if len(str(mes)) == 1:
    mes = str(0) + str(mes)

print('Escriba el valor inicial de la consulta')
inicio = input()
print('Escriba el valor final de la consulta, recuerde que no pueden ser más de 1000 en total')
fin = input()


# In[61]:


consulta_str = "https://api.mercadopublico.cl/APISOCDS/OCDS/listaOCDSAgnoMesTratoDirecto/" + str(año) + '/' +                str(mes) + "/" + str(inicio) + "/" + str(fin)
consulta = requests.get(consulta_str)


# **Obtener links de las distintas licitaciones**

# In[62]:


def jprint(obj):
    text = json.dumps(obj, sort_keys = True, indent=4)
    print(text)

#jprint(consulta.json())

datos = consulta.json()['data']
cantidad = len(datos)

licitaciones = []
for x in range(0, cantidad):
    link = datos[x]['urlAward']
    licitaciones.append(link)


# **Obteniendo info de las licitaciones**

# In[63]:


df = pd.DataFrame(columns = ['Link','Entidad','Descripción','Valor','Status'])

palabras = palabras_claves()

for licitacion in licitaciones:
    consulta = requests.get(licitacion)
    resultado = consulta.json()
    descripcion = resultado['releases'][0]['awards'][0]['description']
    seguir = tiene_claves(palabras, descripcion)
    
    if seguir:
        entidad = resultado['releases'][0]['parties'][0]['name']
        valor = resultado['releases'][0]['awards'][0]['value']['amount']
        status = resultado['releases'][0]['awards'][0]['status']
        
        
        df = df.append({'Link': licitacion, 'Entidad': entidad, 'Descripción': descripcion,'Valor': valor,                        'Status': status},ignore_index = True)
        print('coincide')
    else:
        print('No coincide con lo que buscas')


# In[64]:


df.to_csv('Licitaciones.csv', index = False)


# # Hacer consulta por id de licitación

# In[26]:


print('Escriba id de la licitación')
id_lic = input()


# In[27]:


consulta_str = "https://apis.mercadopublico.cl/OCDS/data/award/" + str(id_lic)
consulta = requests.get(consulta_str)


# In[28]:


def jprint(obj):
    text = json.dumps(obj, sort_keys = True, indent = 4)
    print(text)

jprint(consulta.json())


# In[ ]:




