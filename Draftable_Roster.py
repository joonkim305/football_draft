import pandas as pd


players = pd.read_csv('FP_combined.csv',index_col=0)
players = players.sort_values(by='FP', ascending=0).reset_index()
# ros = pd.read_csv('Roster.csv')
ros = pd.DataFrame({'Pos':['QB','WR','RB','TE'],
                    'Ros':[1,3,2,1]})


t = 14
r = 13

draft_ros = pd.DataFrame()
pos_value = pd.DataFrame()

draft_ros = draft_ros.append(players[players['POS'] == 'QB'].head(n=int(ros.loc[ros['Pos']=='QB','Ros']*t)))

pos_value['POS'] = ['QB','WR','RB','TE','FLX']
pos_value.loc[pos_value['POS']=='QB','Avg'] = draft_ros['FP'].head(t).mean()
pos_value.loc[pos_value['POS']=='QB','Std'] = draft_ros['FP'].head(t).std()


players = players[players['POS']!='QB']

for c in ['QB','WR','RB','TE']:

    if c !='QB':
        dp = players[players['POS'] == c].head(n=int(ros.loc[ros['Pos'] == c, 'Ros'] * t))
        pos_value.loc[pos_value['POS'] == c, 'Avg'] = dp['FP'].mean()
        pos_value.loc[pos_value['POS'] == c, 'Std'] = dp['FP'].std()
        draft_ros = draft_ros.append(dp)
        players = players.loc[~players.index.isin(dp.index)]


draft_ros = draft_ros.append(players.head(n=int(t*r - len(draft_ros))))

for c in ros['Pos']:
    print(c)
    pos_value.loc[pos_value['POS'] == c, 'Avg'] = draft_ros.loc[draft_ros['POS'] == c, 'FP'].mean()
    pos_value.loc[pos_value['POS'] == c, 'Std'] = draft_ros.loc[draft_ros['POS'] == c, 'FP'].std()

pos_value.loc[pos_value['POS'] =='FLX','Avg'] = draft_ros.loc[draft_ros['POS']!='QB','FP'].mean()
pos_value.loc[pos_value['POS'] =='FLX','Std'] = draft_ros.loc[draft_ros['POS']!='QB','FP'].std()

draft_ros.to_csv('draftable.csv')
pos_value.to_csv('Pos_Value.csv')