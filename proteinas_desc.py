import pandas as pd
from os import listdir
from json import load

df = pd.read_csv('df_proteinas_unicas.csv')
df = pd.concat([df, pd.DataFrame(columns=['Name', 'Porcentaje'])])
files = sorted([int(i.split('.')[0]) for i in listdir('./info/') if i[-4:] == 'json'])
for index in range(df.size):
    if index in files:
        with open(f'./info/{index}.json') as file:
            first = load(file)['hits'][0]
            df['Name'].loc[index] = first['hit_desc']
            df['Porcentaje'].loc[index] = first['hit_hsps'][0]['hsp_identity']

df.to_csv('proteinas_desc.csv', index=False)
print(df.head())