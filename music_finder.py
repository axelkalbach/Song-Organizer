import pandas as pd

df = pd.read_excel('file:C:/random/songs.xlsx')

print(df)

for i, row in df.iterrows():
    print(row['Name'])