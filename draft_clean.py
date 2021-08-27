import pandas as pd
import numpy as np

draft = pd.read_csv('draft_price2.csv', encoding='ISO-8859-1')
draft['Price'] = draft['Price'].ffill()


draft = draft.loc[~draft['Player'].str.split(' - ',expand=True)[1].isnull()]

draft['Pos'] = draft['Player'].str.split(' - ',expand=True)[1].str.strip()
draft['Player'] = draft['Player'].str.split(' - ',expand=True)[0].str.strip()
draft['Team'] = draft['Player'].str.split('\xa0',expand=True)[1].str.strip()
draft['Player'] = draft['Player'].str.split('\xa0',expand=True)[0].str.strip()

draft = draft[draft['Price'] != '$-']
draft['Price'] = draft['Price'].astype(float)

draft.to_csv('Player_Price2.csv')