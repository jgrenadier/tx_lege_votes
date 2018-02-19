# -*- coding: utf-8 -*-
"""
lege - a class for reading and manipulating legistrator info
from open states https://openstates.org/

Initially, this class will be used to acess the json files that
can be downloaded in bulk from open states.  Later, I may use the
realtime api to obtain the data.
 
Created on Mon Feb 12 10:09:52 2018

@author: jim grenadier

"""

import os
import json
import pprint


class Lege:
    
    def __init__(self):
        """
            This is the lege initializer
        """
        self._rascals = dict()
        

    # an example relative path for legislator info        
    RASCAL_DIR_PATH_EXAMPLE = "data/2017-07-01-tx-json/legislators"

    @property
    def rascals(self):
        """
        accessor to get rascals cached in the instance
        note:
            not used much since I use alot of lame static methods.
        """ 
        return self._rascals

    @staticmethod
    def rascal_files_to_dict(directory_in_str):
        """
        get legislator info
      
        returns a dictionary where the dictionary keys are the
        unique id for each legislator and each element of the dictionary 
        contains all the equivalent of the json contents of each file/  
        By convention, we will usually place the legislative info files in a 
        sub-directory called "data" within the directory where our code resides.
        
        """
        rascal_dir = os.fsencode(directory_in_str)
        rascals = dict()
        for file in os.listdir(rascal_dir):
            rascal_filename = os.fsdecode(file)
            rascal_prefix, rascal_ext = os.path.splitext(rascal_filename)
            if (rascal_ext == ""):
                rascal_full = os.path.join(directory_in_str, rascal_filename)
                #print("filename = " + rascal_filename)           
                with open(rascal_full) as json_data:
                    d = json.load(json_data)
                    rascals[rascal_prefix] = d
                    #print(d)
                    #e = d["actions"]
                    #print(e[0]['date'])
        return rascals



    def read_rascals_from_disk(self, filepath):
        """
            read all the legislator json files
            and cache the results in an attribute of this instance of Lege
        """
        self._rascals = Lege.rascal_files_to_dict(filepath)
        return


    def format_rascals(self):
        """
            format rascals dictionary nicely to a string for viewing
            by a human.  
            
        """
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pprint(self._rascals)
    
    @staticmethod
    def format_rascal(rascal_dict):
        """
            format rascal dictionary nicely to a string for viewing
            by a human.  
            
        """
        
        # note: an alternative technique might be to convert back to json
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pprint(rascal_dict)
    
    @staticmethod
    def test_read_rascals_from_disk():
        lege1 = Lege()
        lege1.read_rascals_from_disk(Lege.RASCAL_DIR_PATH_EXAMPLE)
       
        for test_rascal, test_rascal_val in lege1.rascals.items():
            print(Lege.format_rascal(test_rascal_val))
            break
        #
        # alternative printing technique
        #
        # print(lege1.format_rascals())
        return
    
# run a test driver
#Lege.test_read_rascals_from_disk()
