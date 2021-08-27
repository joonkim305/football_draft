import pandas as pd

value = pd.read_csv('value.csv', index_col=0)
price = pd.read_csv('Player_Price2.csv',index_col=0, encoding='ISO-8859-1')
name_ex = pd.read_csv('name_ex.csv',index_col=0)

name_exceptions = pd.DataFrame()
n = 0

for p in value['Player']:
    print(p)
    if price.loc[price['Player'] == p,'Price'].empty:
        if name_ex.loc[name_ex['value'] == p, 'price'].empty:
            p_a = input()
            if p_a == 'no':
                value.loc[value['Player'] == p, 'Avg_Price'] = 1
            else:
                value.loc[value['Player'] == p, 'Avg_Price'] = price.loc[price['Player'] == p_a, 'Price']
                name_exceptions.loc[n, 'value'] = p
                name_exceptions.loc[n, 'price'] = p_a
            n = n + 1
        else:
            p_a = name_ex.loc[name_ex['value'] == p, 'price'].values[0]
            value.loc[value['Player'] == p, 'Avg_Price'] = price.loc[price['Player'] == p_a, 'Price'].values[0]

    else:
        value.loc[value['Player'] == p, 'Avg_Price'] = price.loc[price['Player'] == p, 'Price'].values[0]

name_exceptions.to_csv('name_ex_1.csv')
value.to_csv('Value_with_price.csv')