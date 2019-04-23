import numpy as np
import random
import os
import pickle


class BreedGeneration:
    
    
    """
    
    
    A class just used too create the first generation of fighters fr the tournament
    
    
    """
    
    def __init__(self,dead_generation,mutation_rate = 0.1,number_of_fighters = 16, last_name_list_file = 'last-names.txt',first_name_list_file = 'first-names.txt'):
        
        """
        
        Initialize some values mostly with nothings
        
        """
        
        self.dead_generation = dead_generation
        self.generation_number = dead_generation['generation_number']+1
        self.cwd = os.getcwd()
        self.matrix_dimensions = dead_generation['fighters'][list(dead_generation['fighters'].keys())[1]]['attributes'].shape

        
        self.ids = None
        self.generation_dict = dict()
        self.number_of_fighters = number_of_fighters
        self.file_last_name_list = last_name_list_file
        self.file_first_name_list = first_name_list_file
        self.mutation_rate = mutation_rate
        self.gen_storage_location = os.path.abspath(os.path.join(self.cwd,
                                                                 '..', 'storage',
                                                                 'generation_'+str(self.generation_number)+'_pool',
                                                                 'gen'+str(self.generation_number)+'begin.pickle'))
    def createIDList(self):
        self.ids = ["g"+str(self.generation_number)+"_c" + str(num) for num in range(self.number_of_fighters)]
    def pullNameList(self):
        last_name_list_path = os.path.abspath(os.path.join(self.cwd, '..', 'storage','resources',self.file_last_name_list))
        text_file = open(last_name_list_path, "r")
        self.last_name_list = text_file.read().split('\n')
        text_file.close()
        
        first_name_list_path = os.path.abspath(os.path.join(self.cwd, '..', 'storage','resources',self.file_first_name_list))
        text_file = open(first_name_list_path, "r")
        self.first_name_list = text_file.read().split('\n')
        text_file.close()
    def populateProbabilities(self):
        self.indexlist = list(self.dead_generation['fighters'].keys())
        wins = []
        for key in self.indexlist:
            wins.append(self.dead_generation['fighters'][key]['wins'])
        self.fighter_probabilities = np.array(wins)/sum(wins)
    def get_matrix_mask_2(self):
        mask_test = np.full(self.matrix_dimensions[0]**2,True)

        mask_test[0:int(self.matrix_dimensions[0]**2/2)] = False
        np.random.shuffle(mask_test)
        return mask_test.reshape(self.matrix_dimensions)
    def breedFighters(self):
        fighter_1 = self.dead_generation['fighters'][np.random.choice(self.indexlist, p=self.fighter_probabilities)]
        fighter_2 = self.dead_generation['fighters'][np.random.choice(self.indexlist, p=self.fighter_probabilities)]
        #get name
        new_first_name = random.choice(self.first_name_list)
        new_last_name = random.choice([fighter_1['last_name'],fighter_2['last_name']])
        name = new_first_name+' '+new_last_name
        #get masks for equation
        tf1_mask = self.get_matrix_mask_2()
        tf2_mask = np.invert(tf1_mask)
        #create base stats
        base_fighter_attributes = (fighter_1['attributes']*tf1_mask+fighter_2['attributes']*tf2_mask)
        base_fighter_attributes = np.nan_to_num(base_fighter_attributes)
        #mutate base stats
        mutation = np.random.rand(self.matrix_dimensions[0],self.matrix_dimensions[0])-0.5
        new_fighter_attributes = base_fighter_attributes + mutation*self.mutation_rate
        return name, new_last_name, new_fighter_attributes
    def populateDictionary(self):
        self.generation_dict['generation_number']=self.generation_number
        self.generation_dict['mutation_rate']=self.mutation_rate
        self.generation_dict['fighters']=dict()
        for num,i in enumerate(self.ids):
            self.generation_dict['fighters'][i] = dict()
            #create name
            name,last_name, attributes = self.breedFighters()
            #other attributes
            self.generation_dict['fighters'][i]['name'] = name
            self.generation_dict['fighters'][i]['last_name'] = last_name
            self.generation_dict['fighters'][i]['alive'] = 1
            self.generation_dict['fighters'][i]['attributes'] = attributes
            self.generation_dict['fighters'][i]['wins'] = 0
            self.generation_dict['fighters'][i]['tournament_count'] = 0
    def saveDictionary(self):
        with open(self.gen_storage_location, 'wb') as handle:
            pickle.dump(self.generation_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def pipeline(self):
        self.createIDList()
        self.pullNameList()
        self.populateProbabilities()
        self.populateDictionary()
        self.saveDictionary()
