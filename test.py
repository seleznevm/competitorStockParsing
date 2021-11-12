import pandas as pd
from styleframe import StyleFrame, Styler
list1 = "АСУТП"
list2 = "Пром ПК"

df1 = pd.read_excel("NNZ_warehouse.xls", sheet_name=list1, engine="openpyxl")
df2 = pd.read_excel("NNZ_warehouse.xls", sheet_name=list2, engine="openpyxl")
excel_writer = StyleFrame.ExcelWriter("NNZ_warehouse.xlsx")
sf1 = StyleFrame(df1)
sf2 = StyleFrame(df2)
st = Styler(horizontal_alignment="left")

col_style_dict = {
    "Модель": "34",
    "Склад": "19",
    "Количество": "14.5",
    "Тип оборудования": "25",
}

sf1.set_column_width_dict(col_style_dict)
sf1.apply_column_style(["Модель", "Склад", "Тип оборудования"], st)
sf2.set_column_width_dict(col_style_dict)
sf2.apply_column_style(["Модель", "Склад", "Тип оборудования"], st)
sf1.to_excel(excel_writer=excel_writer, columns_and_rows_to_freeze='A1', sheet_name=list1)
sf2.to_excel(excel_writer=excel_writer, columns_and_rows_to_freeze='A1', sheet_name=list2)
excel_writer.save()


