import pandas as pd
df1_e = pd.read_excel('699.xls')
df1_e.to_csv('csv699.csv', index=False, sep=',', encoding='cp1251')
df1 = pd.read_csv('csv699.csv', header=11, usecols=['Товар', 'Кількість'], encoding='cp1251', )
df2 = pd.read_excel('export_products_230725.xlsx', header=1, sheet_name=0, usecols=['Товар', 'К-сть'])
df2.rename(columns={'К-сть': "Кількість"}, inplace=True)

for i in range(len(df2)):
    df2['Кількість'][i] = df2['Кількість'][i].split()[0]

for i in range(len(df1)):
    df1['Кількість'][i] = str(df1['Кількість'][i]).split()[0].replace('.', ',')

my_df = pd.DataFrame(columns=("Товар", "Кількість постачальника", "Кількість замовника"))

for i in range(len(df2)):
    name_article = df2['Товар'][i]
    if name_article not in df1['Товар'].values:
        my_df.loc[len(my_df)] = {"Товар": name_article, "Кількість постачальника": '0', "Кількість замовника": df2['Кількість'][i]}
    else:
        index_article = df1[df1["Товар"]==name_article].index[0]
        if df2['Кількість'][i] != df1['Кількість'][index_article]:
            my_df.loc[len(my_df)] = {"Товар": name_article, "Кількість постачальника": df1['Кількість'][index_article],
                                     "Кількість замовника": df2['Кількість'][i]}

for i in range(len(df1)):
    name_article = df1['Товар'][i]
    if name_article not in df2['Товар'].values:
        my_df.loc[len(my_df)] = {"Товар": name_article, "Кількість постачальника": '0', "Кількість замовника": df1['Кількість'][i]}

my_df = my_df.drop_duplicates(subset=['Товар'])
my_df.to_excel('out_my2.xlsx')

df3 = df1.merge(df2, how='outer', left_on=('Товар'), right_on=('Товар'),
                suffixes=['_Постачальник', '_Замовник'], indicator=True)
df4 = df2.merge(df1, how='outer', left_on=('Товар'), right_on=('Товар'),
                suffixes=['_Замовник', '_Постачальник'], indicator=True)

df5=pd.merge(df3.query("_merge=='right_only'"), df4.query("_merge=='right_only'"), how ='outer', indicator=False).drop_duplicates(subset=['Товар'])
df5.to_excel('out_my.xlsx')

#print(value)

#print(df1)

#file_1 = input("Введіть назву таблиці постачальника ...>>>")
#file_2 = input("Введіть назву таблиці замовника     ...>>>")

