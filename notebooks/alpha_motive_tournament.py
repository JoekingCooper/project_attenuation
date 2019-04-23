import numpy as np
import random
import pickle
def number_of_rounds(n):
    return np.floor(np.log(n)/np.log(2))
"""
DONE:
- reset wins and reset life function so that tournament can be rerun
- test with different matrix sizes

TODO:

- combination of attributes as decider (instead of one) + a weight matrix for that combination




"""

class AlphaMotiveTournament():
    
    
    """
    
    
    The tournament class, hosted by AlphaMotive.
    
    
    """
    
    
    def __init__(self,fighter_dict:"Dictionary with fighter data."):
        
        """
        Initialize for the tournament
        """
        
        
        self.pool_dead = []
        self.pool_2 = []
        self.fighter_dict = fighter_dict.copy()
        self.number_of_rounds = number_of_rounds(len(fighter_dict['fighters']))
        self.pool_1 = list(self.fighter_dict['fighters'].keys())
        self.pool_init = list(self.fighter_dict['fighters'].keys())
        self.fight_number = 0
        dummy_attribute_matrix = self.fighter_dict['fighters'][self.pool_1[0]]['attributes']
        self.att_matrix_dimension_0 = len(dummy_attribute_matrix)-1
        self.att_matrix_dimension_1 = len(dummy_attribute_matrix[0])-1
        
    def single_fight(self,pool,printswitch=True):
        contestant1 = random.choice(pool)
        pool.remove(contestant1)
        contestant2 = random.choice(pool)
        pool.remove(contestant2)
        #get indx mapping for fight, random values are compared to decide the winner.
        inx_0 = random.randint(0, self.att_matrix_dimension_0)
        inx_1 = random.randint(0, self.att_matrix_dimension_1)
        #print names of contestants
        if printswitch:
            print('... Fight',self.fight_number)
            print('... - ',self.fighter_dict['fighters'][contestant1]['name'],'Vs.',self.fighter_dict['fighters'][contestant2]['name'])
        #access the comparison fight values
        contestant1_score = self.fighter_dict['fighters'][contestant1]['attributes'][inx_0][inx_1]
        contestant2_score = self.fighter_dict['fighters'][contestant2]['attributes'][inx_0][inx_1]
        # give winner and looser
        winner = np.where(contestant1_score>=contestant2_score,contestant1,contestant2).item()
        if printswitch:
            print('... - ',self.fighter_dict['fighters'][winner]['name'],'is the winner!')
        loser = np.where(contestant1_score<contestant2_score,contestant1,contestant2).item()
        return winner, loser
    def tournament(self,printswitch=True):
        winner = None
        pool_1 = self.pool_1 
        pool_dead = self.pool_dead
        pool_2 = self.pool_2
        self.fight_number = 0
        for tournament_round in range(int(self.number_of_rounds)):
            #print stage number
            if printswitch:
                print('Stage:',tournament_round)
            for fight_num in range(int(len(pool_1)/2)):
                #run fight
                self.fight_number += 1
                winner, loser = self.single_fight(pool_1,printswitch=printswitch)
                # add winner to next pool
                pool_2.append(winner)
                self.fighter_dict['fighters'][winner]['wins']+=1
                # add loser to pool dead pool
                pool_dead.append(loser)
                self.fighter_dict['fighters'][loser]['alive']=0
                self.fighter_dict['fighters'][loser]['tournament_count']+=1
            pool_1 = pool_2.copy()
            pool_2 = []
        self.pool_1 = pool_1
        self.pool_2 = pool_2
        self.pool_dead = pool_dead
        self.tournament_winner = winner
        self.tournament_winner_stats = self.fighter_dict['fighters'][winner]['attributes']
        self.fighter_dict['fighters'][winner]['tournament_count']+=1
        if printswitch:
            print('The Alpha Motive Champion is',self.fighter_dict['fighters'][self.tournament_winner]['name'])
            print('Kills =',self.fighter_dict['fighters'][self.tournament_winner]['wins'])
    def produceAverageWinner(self):
        fights = self.fighter_dict['fighters'][self.tournament_winner]['wins']
        attribute_addition = self.fighter_dict['fighters'][self.tournament_winner]['wins']*self.fighter_dict['fighters'][self.tournament_winner]['attributes']
        for fighter in self.pool_dead:
            attribute_addition += self.fighter_dict['fighters'][fighter]['wins']*self.fighter_dict['fighters'][fighter]['attributes']
            fights += self.fighter_dict['fighters'][fighter]['wins']
        self.averagewinner_stats = attribute_addition/fights
    def resetPools(self):
        self.pool_dead = []
        self.pool_2 = []
        self.pool_1 = list(self.fighter_dict['fighters'].keys())
    def resetAlive(self):
        for fighter in list(self.fighter_dict['fighters'].keys()):
            self.fighter_dict['fighters'][fighter]['alive']=1
    def resetWins(self):
        for fighter in list(self.fighter_dict['fighters'].keys()):
            self.fighter_dict['fighters'][fighter]['wins']=0
    def resetAll(self):
        self.resetPools()
        self.resetAlive()
        self.resetWins()
        