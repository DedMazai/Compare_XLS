import pandas as pd
df1_e = pd.read_excel('699.xls')
df1_e.to_csv('csv699.csv', index=False, sep=',', encoding='cp1251')
df1 = pd.read_csv('csv699.csv', header=11, usecols=['Товар', 'Кількість'], encoding='cp1251', )
df2 = pd.read_excel('export_products_230725.xlsx', header=1, sheet_name=0, usecols=['Товар', 'К-сть'])
df2.rename(columns={'К-сть': "Кількість"}, inplace=True)
print(df1)

file_1 = input()
