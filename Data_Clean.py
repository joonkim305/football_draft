import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

pos = ['QB','RB','WR','TE']
df_c = pd.DataFrame()

for p in pos:
    df = pd.read_csv('FantasyPros_Fantasy_Football_Projections_' + p + '.csv')
    df = df.dropna()

    for c in df.columns:
        if (c != 'Player') & (c != 'Team'):
            if df[c].dtype == 'object':
                df[c] = df[c].str.replace(',','')
                df[c] = pd.to_numeric(df[c])


    if p == 'QB':
        df = df.rename(columns={'YDS':'PYDS','TDS':'PTDS','YDS.1':'YDS','TDS.1':'TDS'})
        df['REC'] = 0

    if (p == 'RB') | (p == 'WR'):
        df['PYDS'] = 0
        df['PTDS'] = 0
        df['INTS'] = 0
        df['YDS'] = df['YDS'] + df['YDS.1']
        df['TDS'] = df['TDS'] + df['TDS.1']
    if p == 'TE':
        df['PYDS'] = 0
        df['PTDS'] = 0
        df['INTS'] = 0

    df['FP'] = df['PYDS']/25 + df['PTDS']*4 + df['YDS']/10 + df['FL']*-2 + df['TDS'] * 6 + df['REC'] * 0.5 + df['INTS'] * -2
    df['POS'] = p

    df_c = df_c.append(df[['Player','Team','FP','POS']])

df_c.to_csv('FP_combined.csv')