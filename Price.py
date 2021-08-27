import pandas as pd
import reg_jk as rg

players = pd.read_csv('draftable.csv', index_col=0)
pos_value = pd.read_csv('Pos_Value.csv', index_col=0)

for p in players['POS'].unique():
    m = pos_value.loc[pos_value['POS'] == p, 'Avg'].values[0]
    s = pos_value.loc[pos_value['POS'] == p, 'Std'].values[0]

    players.loc[players['POS'] == p,'Value'] = (players['FP'] - m)/s

m = pos_value.loc[pos_value['POS'] == 'FLX', 'Avg'].values[0]
s = pos_value.loc[pos_value['POS'] == 'FLX', 'Std'].values[0]

players['FLX_Value'] = players['Value'].min()

players.loc[players['POS'] != 'QB','FLX_Value'] = (players['FP'] - m)/s

players.loc[players['FLX_Value']>players['Value'],'Value'] = players['FLX_Value']
players = players.sort_values(by='Value', ascending=0).reset_index()

p_curve = pd.read_csv('Avg_Cost.csv')
p_curve = p_curve.head(len(players)).reset_index()

coef = rg.linear_reg(players['Value'],p_curve['Avg Cost'],3)

players['Price'] = players['Value'] ** 3 * coef[3] + players['Value'] ** 2 * coef[2] + players['Value']  * coef[1] + coef[0]

min_v = players.loc[players['Price'].idxmin(),'Value']
print(min_v)
players.loc[players['Value']<=min_v,'Price'] = players.loc[players['Price'].idxmin(),'Price']
players = players.drop(['Value','FLX_Value'], axis=1)
players.to_csv('value.csv')