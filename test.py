import pandas as pd
df = pd.read_excel("ACS.xlsx")

pd.set_option("display.mi", 5)
# print(df)
df.to_excel("ACS_2.xlsx")