import requests
import lxml
import pandas as pd
import re
from bs4 import BeautifulSoup

# ACS links
NNZ_CONTROLLERS = "https://nnz-ipc.ru/catalogue/automation/controllers/?pa=100"
NNZ_MODULES = "https://nnz-ipc.ru/catalogue/automation/io/?pa=100"
NNZ_DAQ_BOARDS = "https://nnz-ipc.ru/catalogue/automation/io_boards/?pa=100"
NNZ_EXP_UNITS = "https://nnz-ipc.ru/catalogue/automation/extension_chassis/?pa=100"
NNZ_SPEC_MODELS = "https://nnz-ipc.ru/catalogue/automation/specialized_modules/?pa=100"
NNZ_DB_BOARDS = "https://nnz-ipc.ru/catalogue/automation/specialized_boards/?pa=100"
NNZ_HMI = "https://nnz-ipc.ru/catalogue/automation/hmi/?pa=100"
NNZ_SENSORS = "https://nnz-ipc.ru/catalogue/automation/remote_data_logger/?pa=100"
NNZ_ACCESSORIES = "https://nnz-ipc.ru/catalogue/automation/automation_accesories/?pa=100"

# COMM links
NNZ_ETHERNET = "https://nnz-ipc.ru/catalogue/comm/ethernet/?pa=100"
NNZ_SERIAL_SERVERS = "https://nnz-ipc.ru/catalogue/comm/serial_to_ethernet/?pa=100"
NNZ_MULTIBOARD = "https://nnz-ipc.ru/catalogue/comm/serial/?pa=100"
NNZ_WIRELESS = "https://nnz-ipc.ru/catalogue/comm/wireless/?pa=100"
NNZ_CONVERTERS = "https://nnz-ipc.ru/catalogue/comm/converters/?pa=100"
NNZ_SOFTWARE = "https://nnz-ipc.ru/catalogue/comm/software/?pa=100"
NNZ_COMM_ACCESSORIES = "https://nnz-ipc.ru/catalogue/comm/network_accesories/?pa=100"
NNZ_COMM_ACCESSORIES2 = "https://nnz-ipc.ru/catalogue/comm/accessories/?pa=100"

# PromPC links
NNZ_EMBEDDED = "https://nnz-ipc.ru/catalogue/ipc/embedded_pc/?pa=100"
NNZ_PANELPC = "https://nnz-ipc.ru/catalogue/ipc/panel_pc/?pa=100"
NNZ_COMPUTERS = "https://nnz-ipc.ru/catalogue/ipc/computers/?pa=100"
NNZ_DIGSIGNAGE = "https://nnz-ipc.ru/catalogue/ipc/digital_signage/?pa=100"
NNZ_CPU_BOARDS = "https://nnz-ipc.ru/catalogue/ipc/processor_boards/?pa=100"
NNZ_PASSIVE_BOARDS = "https://nnz-ipc.ru/catalogue/ipc/backplane/?pa=100"

ACS_COMM_list = [NNZ_CONTROLLERS, NNZ_MODULES, NNZ_DAQ_BOARDS, NNZ_EXP_UNITS, NNZ_SPEC_MODELS, NNZ_DB_BOARDS, NNZ_HMI, NNZ_SENSORS, NNZ_ACCESSORIES, NNZ_ETHERNET, NNZ_SERIAL_SERVERS, NNZ_MULTIBOARD, NNZ_WIRELESS, NNZ_CONVERTERS, NNZ_SOFTWARE, NNZ_COMM_ACCESSORIES, NNZ_COMM_ACCESSORIES2]
PROM_PC_list = [NNZ_EMBEDDED, NNZ_PANELPC, NNZ_COMPUTERS, NNZ_DIGSIGNAGE, NNZ_CPU_BOARDS, NNZ_PASSIVE_BOARDS]

ACS_COMM_list_s = ["NNZ_CONTROLLERS", "NNZ_MODULES", "NNZ_DAQ_BOARDS", "NNZ_EXP_UNITS", "NNZ_SPEC_MODELS", "NNZ_DB_BOARDS", "NNZ_HMI", "NNZ_SENSORS", "NNZ_ACCESSORIES", "NNZ_ETHERNET", "NNZ_SERIAL_SERVERS", "NNZ_MULTIBOARD", "NNZ_WIRELESS", "NNZ_CONVERTERS", "NNZ_SOFTWARE", "NNZ_COMM_ACCESSORIES", "NNZ_COMM_ACCESSORIES2"]
PROM_PC_list_s = ["NNZ_EMBEDDED", "NNZ_PANELPC", "NNZ_COMPUTERS", "NNZ_DIGSIGNAGEMб", "NNZ_CPU_BOARDS", "NNZ_PASSIVE_BOARDS"]
############## internal request ##############
# with open("NNZ_IN.htm", encoding="utf8") as f:
#     page = BeautifulSoup(f, "lxml")

############## extrenal request ##############
# url = "https://nnz-ipc.ru/catalogue/comm/ethernet/?pa=300&sort=available"
# r = requests.get(url)
# page = BeautifulSoup(r.text, "lxml")

WH_List = []
model_list = []
zero = 0

def parsing(list):
    global zero
    for url in list:
        r = requests.get(url)
        page = BeautifulSoup(r.text, "lxml")
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
                dict = {"Склад": str(warehouse), "Количество": str(qty), "Тип оборудования": ACS_COMM_list_s[zero]}
                WH_List.append(dict)
                model_list.append(model)
        zero += 1

parsing(ACS_COMM_list)
df1 = pd.DataFrame(WH_List, index= model_list, columns= ["Склад", "Количество", "Тип оборудования"], dtype="string")
df1.index.name = "Модель"

WH_List = []
model_list = []
zero = 0

parsing(PROM_PC_list)
df2 = pd.DataFrame(WH_List, index= model_list, columns= ["Склад", "Количество", "Тип оборудования"], dtype="string")
df2.index.name = "Модель"

with pd.ExcelWriter("NNZ_warehouse.xlsx") as writer:
    df1.to_excel(writer, sheet_name="АСУТП")
    df2.to_excel(writer, sheet_name="Пром ПК")

