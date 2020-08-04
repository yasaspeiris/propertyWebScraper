import pandas as pd
import requests
from bs4 import BeautifulSoup
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

link_base = "https://ikman.lk"

df = pd.DataFrame()

for i in range(1,99):
    res = requests.get(link_base+"/en/ads/colombo/land?by_paying_member=0&sort=date&order=desc&buy_now=0&urgent=0&page="+str(i))
    soup = BeautifulSoup(res.content,'lxml')
    for ultag in soup.find_all('ul', {"class": lambda x: x and x.startswith("list--")}):
        for litag in ultag.find_all('li',{"class": lambda x: x and x.startswith("normal--")}):
            for adcontainer in litag.find_all('a', {"class": lambda x: x and x.startswith("card-link--")}):

                href =  (link_base+adcontainer['href'])
                title =  (adcontainer['title'])

                #price
                price = ""
                per = ""
                for pricetag in adcontainer.find_all('div', {"class": lambda x: x and x.startswith("price--")}):
                    try:
                        split_list = pricetag.text.split()
                        price = locale.atoi(split_list[1])
                        per = split_list[2] + " "+split_list[3] 
                    except:
                        pass

                #location
                location = ""
                for subtitle in adcontainer.find_all('div', {"class": lambda x: x and x.startswith("description--")}):
                    location = (subtitle.text)
                
                #perches
                perches = ""
                for perches in adcontainer.find_all('div',{'class': None}):
                    if perches.text.endswith("perches"):
                        perches = (perches.text)

                data = {
                    "Title" : title,
                    "Location" : location,
                    "Perches" : perches,
                    "Price": price,
                    "Per" : per,
                    "Link" : href
                    
                }

                df = df.append(data,ignore_index=True)
    
    print("Scraped Page "+str(i))

columnsTitles = ['Title','Location','Perches','Price','Per','Link']
df = df.reindex(columns=columnsTitles)
print (df)
df.to_excel('Output_V3.xls')
