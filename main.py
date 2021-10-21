import requests
import lxml
from bs4 import BeautifulSoup

url = "https://moxa.ru/shop/ethernet/unmanaged/fast_ethernet/eds-200a/eds-205a/eds-205a/"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
warehouse = soup.find_all("div", class_ = "avail_popup")
print(warehouse)