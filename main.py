import requests
import lxml
import pandas as pd
import re
from bs4 import BeautifulSoup
#TODO: Get data to a variable

############## internal request ##############
with open("NNZ_IN.htm", encoding="utf8") as f:
    page = BeautifulSoup(f, "lxml")

############## extrenal request ##############
# url = "https://nnz-ipc.ru/catalogue/comm/ethernet/?pa=300&sort=available"
# r = requests.get(url)
# page = BeautifulSoup(r.text, "lxml")

WH_List = []
model_list = []
page_list = page.find_all("div", class_ = "catcard_desc")
for n in range(0, len(page_list)):
    # TMP: getting the model name
    page_model = page_list[n].find_all("meta", itemprop = "model")
    model = re.search("\".+?\"", str(page_model))
    model = model.group()
    model = re.sub("\"", "", str(model)) # here we got a clear model name
    page_warehouse = page_list[n].find_all("li") # now let's deal with the stock information
    for w in range(0,len(page_warehouse)):
        #getting the warehouse name
        warehouse = page_warehouse[w].span.children  #TODO: 2. think how to pass the EOL models
        for child in warehouse:
            warehouse = child # here we got the clear city name of the warehouse
        qty = page_warehouse[w].b.children
        for child in qty:
            qty = child
        if warehouse == "Замена от производителя":
            break
        dict = {"Склад": str(warehouse), "Количество": str(qty)}
        WH_List.append(dict)
        model_list.append(model)


df = pd.DataFrame(WH_List, index= model_list, columns= ["Склад", "Количество"], dtype="string")
df.index.name = "Модель"
df.to_excel("info2.xlsx")
print(df)