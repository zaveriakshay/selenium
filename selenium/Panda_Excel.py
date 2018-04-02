import pandas as pd


df = pd.read_excel("test/data/Topups_FI_Sample.xlsx")
print (str(df["FICode"].count())+":"+str(df["Amount"].sum())+":"+str(df["TransactionXML"].sum()))

grouped = df.groupby('FICode')

for name,group in grouped:
    print(name)
    print(group)
    print(str(group["FICode"].count()) + ":" + str(group["Amount"].sum()) + ":" + str(group["TransactionXML"].sum()))

df.head()