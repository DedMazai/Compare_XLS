import pandas as pd

data_importer = pd.read_excel('699.xls', header=11, usecols=['Товар', 'Кількість'])
data_client = pd.read_excel('export_products_230725.xlsx', header=1, usecols=['Товар', 'К-сть'], sheet_name=0)

data_client.rename(columns={'К-сть': "Кількість"}, inplace=True)

data_importer.dropna(subset=['Товар', 'Кількість'], inplace=True)
data_client.dropna(subset=['Товар', 'Кількість'], inplace=True)

data_importer['Кількість'] = data_importer['Кількість'].apply(lambda x: float(x))
data_client['Кількість'] = data_client['Кількість'].apply(lambda x: float(x.split(' ')[0].replace(',', '.')))

data_with_values = data_importer.merge(data_client, how='outer', on='Товар',
                                       suffixes=('_постач', '_замов'))

data_with_values = data_with_values[data_with_values['Кількість_постач'] != data_with_values['Кількість_замов']]
data_with_values = data_with_values.fillna(0)
data_with_values['Різниця_кількість'] = abs(data_with_values['Кількість_постач'] - data_with_values['Кількість_замов'])

data_with_values = data_with_values.loc[data_with_values['Різниця_кількість'] > data_with_values['Кількість_замов'] * 0.2]

data_with_values.to_excel('difference.xlsx')
