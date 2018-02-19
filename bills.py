# -*- coding: utf-8 -*-
"""
Bills - a class for reading and manipulating bill info
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


class Bills:
    
    def __init__(self):
        """
            This is the bill initializer
        """
        self._bills_dict = dict()
        

    # an example relative path for legislator info        
    RASCAL_DIR_PATH_EXAMPLE = "data/2017-07-01-tx-json/legislators"
    # an example relative path for bills info 
    BILLS_EXAMPLE_PATH = "data/2017-07-01-tx-json/bills/tx/833/lower"
    
    # directory for bills for the state of Texas
    BILLS_PATH = "data/2017-07-01-tx-json/bills/tx"
    
    @property
    def bill_dict(self):
        """
        accessor to get bills data cached in the instance
        """ 
        return self._bills_dict

    @staticmethod
    def listdirs(path):
        """
        based on: https://stackoverflow.com/questions/31049648/how-to-get-list-of-subdirectories-names
        """
        return [d for d in os.listdir(path) if os.path.isdir(d)]

    @staticmethod
    def build_session_list(directory_in_str):
        """
        let's try to infer the list of available legislative sessions
        from the file names of the directories that are available.
        """
        bills_dir = os.fsencode(directory_in_str)
        sessions = list()
        for file in os.listdir(bills_dir):
            bill_filename = os.fsdecode(file)
            sessions.append(bill_filename)
        return sessions

    @staticmethod
    def bill_files_to_dict(directory_in_str):
        """
        Get bills info from a single directory
        in the form of a dictionary where the dictionary keys are the
        unique id for each legislator.
        """
        #print("+++get_bills(" + directory_in_str + ")")
        bills_dir = os.fsencode(directory_in_str)
        bills = dict()
        for file in os.listdir(bills_dir):
            bill_filename = os.fsdecode(file)        
            bill_full = os.path.join(directory_in_str, bill_filename)
            if (os.path.isdir(bill_full)):
                # nothing for now
                pass
            else:
                bill_prefix, bill_ext = os.path.splitext(bill_filename)                        
                if (bill_ext == ""):
                    bill_full = os.path.join(directory_in_str, bill_filename)
                    #print("filename = " + bill_filename)           
                    with open(bill_full) as json_data:
                        try:
                            d = json.load(json_data)
                            bills[bill_filename] = d
                        except:
                            print("$$$  problem with " + bill_full)
                #print(d)
                #e = d["actions"]
                #print(e[0]['date'])
        return bills
 
    @staticmethod
    def bill_files_to_dict_recursive(directory_in_str):
        """
        get bills recursively from a directory and all sub directories
        """
        #print("---get_bills_recursive(" + directory_in_str + ")")
        bills1 = dict()
        if (not os.path.isdir(directory_in_str)):
            return bills1
        bills1 = Bills.bill_files_to_dict(directory_in_str)
        dirs = os.listdir(directory_in_str)
        for direc2 in dirs:
            direc2_full = os.path.join(directory_in_str, direc2)
            bills2 = Bills.bill_files_to_dict_recursive(direc2_full)
            bills1.update(bills2)
        return bills1



    def read_bills_from_disk(self, filepath):
        """
            read all the bill json files
            and cache the results in an attribute of this instance of Lege
        """
        self._bills_dict = Bills.bill_files_to_dict(filepath)
        return


    def format_bills(self):
        """
            format billss dictionary nicely to a string for viewing
            by a human.  
            
        """
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pprint(self._bills_dict)
    
    @staticmethod
    def format_bill(rascal_dict):
        """
            format bill dictionary nicely to a string for viewing
            by a human.  
            
        """
        
        # note: an alternative technique might be to convert back to json
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pprint(rascal_dict)
    
    @staticmethod
    def test_read_bills_from_disk():
        bills1 = Bills()
        bills1.read_bills_from_disk(Bills.BILLS_EXAMPLE_PATH)
       
        for test_bill, test_bill_val in bills1.bill_dict.items():
            print(Bills.format_bill(test_bill_val))
            break
        #
        # alternative printing technique
        #
        # print(lege1.format_rascals())
        return
    
    @staticmethod
    def test_session_list():
        session_list = Bills.build_session_list(Bills.BILLS_PATH)
        print(session_list)
    
# run a test driver
#Bills.test_read_bills_from_disk()
#Bills.test_session_list()
