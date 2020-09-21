#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup

r=requests.get("http://pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c=r.content
soup=BeautifulSoup(c, "html.parser")
page_nr=soup.find_all("a", {"class":"Page"})
page_nr=page_nr[-1].text
#print(page_nr)


# In[2]:


l=[]
base_url="http://pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s=" #+ ".html"
for page in range(0,int(page_nr)*10,10):
    print(base_url + str(page) + ".html")
    r=requests.get((base_url + str(page) + ".html"),headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c=r.content
    soup=BeautifulSoup(c, "html.parser")
    #print(soup.prettify())
    all=soup.find_all("div", {"class":"propertyRow"})

    for item in all:
        d={}
        try:
            d["Address"]=item.find_all("span", {"class":"propAddressCollapse"})[0].text
        except:
             d["Address"]=None
        try:
            d["Locality"]=item.find_all("span", {"class":"propAddressCollapse"})[1].text
        except:
            d["Locality"]=None
        
        d["Price"]=item.find("h4", {"class":"propPrice"}).text.replace("\n","").replace(" ","")
        
        try:
            d["Beds"]=item.find("span", {"class":"infoBed"}).find("b").text #looking for b tags only
        except:
            d["Beds"]=None #pass
        try:
            d["Area"]=item.find("span", {"class":"infoSqFt"}).find("b").text #looking for b tags only
        except:
            d["Area"]=None #pass
        try:
            d["Full Bath"]=item.find("span", {"class":"infoValueFullBath"}).find("b").text #looking for b tags only
        except:
            d["Full Bath"]=None #pass
        try:
            d["Half Baths"]=item.find("span", {"class":"infoValueHalfBath"}).find("b").text #looking for b tags only
        except:
            d["Half Baths"]=None #pass
        for column_group in item.find_all("div", {"class":"columnGroup"}):
            #print(column_group)
            #print(column_group.find_all("span", {"class":"featureGroup"}))
            #print(column_group.find_all("span", {"class":"featureName"}))
            for feature_group, feature_name in zip(column_group.find_all("span", {"class":"featureGroup"}),column_group.find_all("span", {"class":"featureName"})):
                #print(feature_group.text, feature_name.text)
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]=feature_name.text
    
        l.append(d)


# In[3]:


import pandas
df=pandas.DataFrame(l)


# In[4]:


df

