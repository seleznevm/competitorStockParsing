import requests
import lxml
import pandas as pd
import re
from bs4 import BeautifulSoup

MSK = 'Москва'
SPB = 'Санкт-Петербург'
NSB = 'Новосибирск'
global warehouse_MSK
warehouse_MSK = 0
warehouse_SPB = 0
warehouse_NSB = 0

with open("EDS-408A.htm", encoding="utf8") as f:
    page = BeautifulSoup(f, "lxml")

page_list = page.find_all("li")
model = page.find("h1", class_ = "pagetitle")

print(model)

# TODO: Create the pandas table and insert the values
try:
    data = pd.read_excel(r'NNZ_moxa_warehouse.xlsx')
except:
    print("Can't read the file")



#### enumerate all lines and find the match with patterns ###
def find_stock(pattern):
    for i in range(0, len(page_list)):
        a = re.search(pattern, str(page_list[i]))
        if str(a) != "None":
            qty = re.findall('[0-9][0-9]+\+', str(page_list[i])) or re.findall('[0-9]', str(page_list[i]))
            return qty

warehouse_MSK = find_stock(MSK)
warehouse_SPB = find_stock(SPB)
warehouse_NSB = find_stock(NSB)


############## extrenal request ##############
# url = "https://moxa.ru/shop/ethernet/unmanaged/fast_ethernet/eds-200a/eds-205a/eds-205a/"
# r = requests.get(url)
# soup = BeautifulSoup(r.text, "lxml")
# warehouse = soup.find_all("div", class_ = "avail_popup")
# print(warehouse)