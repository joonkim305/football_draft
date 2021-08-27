import pandas as pd
import numpy as np
import copy
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def lineup(filename, myroster, budget, multiple):


   max_salary = budget - myroster['Salary'].sum()
   empty_roster = myroster[pd.isna(myroster['Player'])]
   filled_roster = myroster.dropna()



   player = pd.read_csv('Value_with_price.csv', index_col = [0])
   player.loc[player['POS']=='QB','Avg_Price'] = player['Price']
   #player = player[player['Drafted']==0]
   player = player.rename(columns={'Avg_Price': 'Salary', 'POS': 'Pos'})
   player['Salary'] = player['Salary']*multiple
   player['FPPS'] = player['FP'] / player['Salary']

   player = player.sort_values(by='FPPS', ascending = 0)
   # FPPS = Fantasy Point per Salary

   org_player = copy.deepcopy(player)

   positions = ['QB','TE','RB','WR','FLX']

   cur_salary = 0
   best_roster = 0
   benched_name = []

   try_bench = 0

   while try_bench < len(empty_roster):

       pos_list = {}

       for i in range(0, len(positions)):

           if positions[i] != 'FLX':
               pos_list['{0}'.format(i)] = player[player['Pos'] == positions[i]]
               pos_list['{0}'.format(i)].index = range(0, len(pos_list['{0}'.format(i)]))
           else:
               pos_list['{0}'.format(i)] = player[player['Pos'] != 'QB']
               pos_list['{0}'.format(i)].index = range(0, len(pos_list['{0}'.format(i)]))
       # Creating player list for each position


       roster = pd.DataFrame()
       for i in range(0, len(positions)):
           l = len(empty_roster[empty_roster['Ros_Pos'] == positions[i]].index)

           if positions[i] == 'FLX':
               pos_list[str(i)] = pos_list[str(i)][~pos_list[str(i)]['index'].isin(roster['index'])]
               pos_roster = pos_list[str(i)].head(l)
               pos_roster.loc[:,'Ros_Pos'] = positions[i]
           else:

               pos_roster = pos_list[str(i)].head(l)
               pos_roster.loc[:,'Ros_Pos'] = positions[i]
           roster = roster.append(pos_roster)
       # Need 2 players for WR, RB, and 1 for QB, TE, FLX
       # Start with the value lineup (highest FPPS)

       roster.index = range(0,len(roster))

       cur_salary = roster['Salary'].sum()

       if cur_salary <= max_salary:

           player_left = player

           for i in range(0, len(roster)):
               player_left = player_left.drop(player_left[player_left['Player'] == roster.loc[i,'Player']].index)
           # Make list of left players



           player_left.index = range(0, len(player_left))

           for i in range(0, len(player_left)):
               if player_left.loc[i,'Pos'] == 'QB':
                   roster_pos = roster[roster['Ros_Pos'] == player_left.loc[i,"Pos"]]
               else:
                   roster_pos = roster[(roster['Ros_Pos'] == player_left.loc[i, "Pos"]) | (roster['Ros_Pos'] == 'FLX')]
               # Players currently on the roster for currently evaluated player's position



               rep_value = 0
               r_index = np.nan
               for j in roster_pos.index.values:
                   if player_left.loc[i,'Salary'] - roster_pos.loc[j,'Salary'] == 0:
                       denom = 0.0001
                   else:
                       denom = player_left.loc[i,'Salary'] - roster_pos.loc[j,'Salary']
                   cur_value = (player_left.loc[i,'FP'] - roster_pos.loc[j, 'FP'])/denom

                   if player_left.loc[i,'FP'] > roster_pos.loc[j, 'FP'] and cur_value > rep_value:
                       rep_value = cur_value
                       r_index = int(j)
               # For each left over player, checking which of currently rostered players has better replacement value
               # If left over player A has FFP 30 $3000 and two rostered players 1,2 are FFP 26, 20 and Salary $1200, $1000,
               # the replacement value A over 1 is (30 - 26)/($3000 - $1200) = 0.0022 and A over 2 is 0.0050,
               # so if we are to insert A into the line up, we need to swap A for 2.


               player_left.loc[i,"Rep_Value"] = rep_value
               player_left.loc[i,"Rep_Roster"] = r_index
               # Store each left over player's replacement value and the player to be replaced in the roster


           replaced = True

           while replaced == True:

               player_left = player_left.sort_values(by="Rep_Value", ascending = 0)
               player_left.index = range(0,len(player_left))
               # Sort here to give priority on player with highest replacement value
               # Check until either find replacement or go through every player on the list

               replaced = False
               i = 0
               while replaced == False and i < len(player_left):
                   if player_left.loc[i,'Rep_Value'] > 0:
                   # Only evaluate the players with positive replacement value

                       r_i = int(player_left.loc[i,"Rep_Roster"])
                       # Roster player index with best replacement value

                       if (max_salary - cur_salary) >= (player_left.loc[i,"Salary"] - roster.loc[r_i,"Salary"]):
                       # if salary increase is within the max salary, replace the player or go the next best option

                           pos_temp = roster.loc[r_i,'Ros_Pos']
                           dropped_player = copy.deepcopy(roster.loc[r_i,:])

                           roster.loc[r_i,:] = player_left.loc[i,:]
                           roster.loc[r_i,'Ros_Pos'] = pos_temp
                           replaced = True
                           cur_salary = roster['Salary'].sum()

                           player_left = player_left.drop(i)
                           # Remove the picked player from the list
                           player_left = player_left.append(dropped_player)
                           player_left.index = range(0,len(player_left))

                           # Once we replace a player on the roster, we have to go through everybody with same position and
                           # re-evaluate their replacement value based on the changed roster


                           for p in range(0, len(player_left)):
                               if player_left.loc[p, 'Pos'] == 'QB':
                                   roster_pos = roster[roster['Ros_Pos'] == player_left.loc[p, "Pos"]]
                               else:
                                   roster_pos = roster[(roster['Ros_Pos'] == player_left.loc[p, "Pos"]) | (roster['Ros_Pos'] == 'FLX')]

                               if (player_left.loc[p, "Pos"] == roster.loc[r_i, "Ros_Pos"]) | ((player_left.loc[p, "Pos"] != 'QB') & (roster.loc[r_i, "Ros_Pos"] == 'FLX')):

                                   rep_value = 0
                                   r_index = np.nan
                                   for j in roster_pos.index.values:

                                       if player_left.loc[p, 'Salary'] - roster_pos.loc[j, 'Salary'] == 0:
                                           denom = 0.0001
                                       else:
                                           denom = player_left.loc[p, 'Salary'] - roster_pos.loc[j, 'Salary']

                                       cur_value = (player_left.loc[p,'FP'] - roster_pos.loc[j, 'FP'])/ denom
                                       if player_left.loc[p,'FP'] > roster_pos.loc[j, 'FP'] and cur_value > rep_value:
                                           rep_value = cur_value
                                           r_index = int(j)

                                   player_left.loc[p,"Rep_Value"] = rep_value
                                   player_left.loc[p,"Rep_Roster"] = r_index


                           #player_left.index = range(0,len(player_left))


                   i = i + 1



           cols = ['FP','Player','Ros_Pos','Pos','Salary']
           if roster['FP'].sum() > best_roster:
               roster_max = copy.deepcopy(roster)
               best_roster = roster['FP'].sum()


       found = False
       try_bench = 0

       roster_min_FFP = roster.sort_values(by='FP')
       roster_min_FFP.index = range(0,len(roster_min_FFP))

       while found == False and try_bench < len(roster):
           if any(roster_min_FFP.loc[try_bench, 'Player'] in s for s in benched_name) == False:
               benched_name.append(roster_min_FFP.loc[try_bench, 'Player'])
               found = True
           else:
               try_bench = try_bench + 1



       if found == True:
           player = org_player.loc[org_player['Player'] != roster_min_FFP.loc[try_bench , 'Player'], :]

   roster_max = roster_max.loc[:,cols]
   roster_max = roster_max.append(filled_roster)
   print(roster_max)
   print(roster_max['Salary'].sum())
   print(roster_max['FP'].sum())


   roster_max.to_csv(filename + '.csv')
   return 0

#lineup('testing')

if __name__ == "__main__":
    myroster = pd.read_csv('myroster.csv')
    budget = 190

    multiple = 1.2
    print(lineup('roster', myroster, budget, multiple))
