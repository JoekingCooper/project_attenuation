import numpy as np
import random
import os
import pickle


class CreateGeneration0:
    
    
    """
    
    
    A class just used too create the first generation of fighters fr the tournament
    
    
    """
    
    def __init__(self,number_of_fighters = 16, last_name_list_file = 'last-names.txt',first_name_list_file = 'first-names.txt',attribute_dimensions = 2):
        
        """
        
        Initialize some values mostly with nothings
        
        """
        self.cwd = os.getcwd()
        self.ids = None
        self.name_list = None
        self.generation0 = dict()
        self.number_of_fighters = number_of_fighters
        self.file_last_name_list = last_name_list_file
        self.file_first_name_list = first_name_list_file
        self.attribute_dimensions = attribute_dimensions
        self.gen0_storage_location = os.path.abspath(os.path.join(self.cwd, '..', 'storage','base','data_dict_gen0.pickle'))
    def createIDList(self):
        self.ids = ["g1_c" + str(num) for num in range(self.number_of_fighters)]
    def pullNameList(self):
        last_name_list_path = os.path.abspath(os.path.join(self.cwd, '..', 'storage','resources',self.file_last_name_list))
        text_file = open(last_name_list_path, "r")
        self.last_name_list = text_file.read().split('\n')
        text_file.close()
        
        first_name_list_path = os.path.abspath(os.path.join(self.cwd, '..', 'storage','resources',self.file_first_name_list))
        text_file = open(first_name_list_path, "r")
        self.first_name_list = text_file.read().split('\n')
        text_file.close()
    def populateDictionary(self):
        self.generation0['generation_number']=0
        self.generation0['mutation_rate']=0
        self.generation0['fighters']=dict()
        for num,i in enumerate(self.ids):
            self.generation0['fighters'][i] = dict()
            #create name
            last_name = random.choice(self.last_name_list) 
            first_name = random.choice(self.first_name_list) 
            self.generation0['fighters'][i]['name'] = first_name+' '+last_name
            self.generation0['fighters'][i]['last_name'] = last_name
            #remove used names
            self.first_name_list.remove(first_name)
            self.last_name_list.remove(last_name)
            #other attributes
            self.generation0['fighters'][i]['alive'] = 1
            self.generation0['fighters'][i]['attributes'] = np.random.rand(self.attribute_dimensions,self.attribute_dimensions)
            self.generation0['fighters'][i]['wins'] = 0
            self.generation0['fighters'][i]['tournament_count'] = 0
    def saveDictionary(self):
        with open(self.gen0_storage_location, 'wb') as handle:
            pickle.dump(self.generation0, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def pipeline(self):
        self.createIDList()
        self.pullNameList()
        self.populateDictionary()
        self.saveDictionary()