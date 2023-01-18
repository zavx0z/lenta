import pandas as pd

df = pd.read_parquet('store/softDrinks.parquet')
df.to_excel('softDrinks.xlsx')
