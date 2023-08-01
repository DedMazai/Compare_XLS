import pandas as pd
data_xls = pd.read_excel('699.xls')
data_xls.to_csv('csv699.csv', index=False, sep=',', encoding='cp1251')
data_importer = pd.read_csv('csv699.csv', header=11, usecols=['Товар', 'Кількість'], encoding='cp1251')
data_client = pd.read_excel('export_products_230725.xlsx', header=1, usecols=['Товар', 'К-сть'], sheet_name=0)
data_client.rename(columns={'К-сть': "Кількість"}, inplace=True)

for i in range(len(data_client)):
    data_client['Кількість'][i] = data_client['Кількість'][i].split()[0]

for i in range(len(data_importer)):
    data_importer['Кількість'][i] = str(data_importer['Кількість'][i]).split()[0].replace('.', ',')

my_df = pd.DataFrame(columns=["Товар", "Кількість постачальника", "Кількість замовника"])

for i in range(len(data_client)):
    name_article = data_client['Товар'][i]
    if name_article not in data_importer['Товар'].values:
        my_df.loc[len(my_df)] = {"Товар": name_article, "Кількість постачальника": '0',
                                 "Кількість замовника": data_client['Кількість'][i]}
    else:
        index_article = data_importer[data_importer["Товар"] == name_article].index[0]
        if data_client['Кількість'][i] != data_importer['Кількість'][index_article]:
            my_df.loc[len(my_df)] = {"Товар": name_article, "Кількість постачальника":
                                     data_importer['Кількість'][index_article],
                                     "Кількість замовника": data_client['Кількість'][i]}

for i in range(len(data_importer)):
    name_article = data_importer['Товар'][i]
    if name_article not in data_client['Товар'].values:
        my_df.loc[len(my_df)] = {"Товар": name_article,
                                 "Кількість постачальника": '0',
                                 "Кількість замовника": data_importer['Кількість'][i]}

my_df = my_df.drop_duplicates(subset=['Товар'])
my_df.to_excel('out_my2.xlsx')

merge_importer_client = data_importer.merge(data_client, how='outer', left_on='Товар', right_on='Товар',
                                            suffixes=('_Постачальник', '_Замовник'), indicator=True)
merge_client_importer = data_client.merge(data_importer, how='outer', left_on='Товар', right_on='Товар',
                                          suffixes=('_Замовник', '_Постачальник'), indicator=True)

merged_data = pd.merge(merge_importer_client.query("_merge=='right_only'"),
                       merge_client_importer.query("_merge=='right_only'"),
                       how='outer', indicator=False).drop_duplicates(subset=['Товар'])
merged_data.to_excel('out_my.xlsx')

# print(value)

# print(data_importer)

# file_1 = input("Введіть назву таблиці постачальника ...>>>")
# file_2 = input("Введіть назву таблиці замовника     ...>>>")
