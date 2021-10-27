import requests
import lxml
import pandas as pd
import re
from bs4 import BeautifulSoup

with open("NNZ_IN.htm", encoding="utf8") as f:
    page = BeautifulSoup(f, "lxml")

page_list = page.find_all("div", class_ = "catcard_desc")

# TMP: getting the model name
page_tmp = page_list[0].find_all("meta", itemprop = "model")
model = re.search("\".+?\"", str(page_tmp))
model = model.group()
model = re.sub("\"", "", str(model))

#getting the warehouse name and q'ty
page_tmp = page_list[0].find("li")
warehouse = page_tmp.span.children
for child in warehouse:
    warehouse = child

qty = page_tmp.b.children
for child in qty:
    qty = child
#TODO: 1. continue to list page_tmp and find warehouses and qties

# TODO: Create the pandas table and insert the values
try:
    data = pd.read_excel(r'NNZ_moxa_warehouse.xlsx')
except:
    print("Can't read the file")


############## extrenal request ##############
# url = "https://moxa.ru/shop/ethernet/unmanaged/fast_ethernet/eds-200a/eds-205a/eds-205a/"
# r = requests.get(url)
# soup = BeautifulSoup(r.text, "lxml")
# warehouse = soup.find_all("div", class_ = "avail_popup")
# print(warehouse)