# -*- coding: utf-8 -*-
"""

keeps track of legislators who dont vote on bills

Created on Tue Feb 13 18:50:56 2018

@author: jim grenadier
"""
#import os
import lege
import bills

class LazyLege(lege.Lege):
    """
    subclass of Lege with logic to build attributes that keep track
    of which bills the legislator have an opportunity to vote on but
    didnt bother to vote.

    notes:    
    Given my current overuse of static methods, this constructor is
    not realy used yet.
    """
    def __init__(self):
        """
            constructor
        """
        super(LazyLege, self).__init__()
        return
    
    @staticmethod
    def leg_id_in_list(lege_list, rascal_id):
        """
        determine if legislator id (usually from a bill attribute)
        is available in a list of legislators
        """
        if not lege_list:
            return False
        for my_lege in lege_list:
            if not my_lege:
                continue
            if not my_lege["leg_id"]:
                continue
            #print(my_lege["leg_id"] + " " + rascal_id )
            if my_lege["leg_id"] == rascal_id:
                #print("!!" + my_lege["leg_id"] + " " + rascal_id )
                return True
        return False
    
    @staticmethod
    def find_wimpy_bills(bills1, key_lege_id):
        """
        create a list of bills that were not voted on by a given
        legislator.
        """
        wimpy_bills_list = list()
        yes_bills_list = list()
        no_bills_list = list()
        for key_bill_id, value_bill_deets in bills1.items():
            votes = value_bill_deets["votes"]
            if not votes:
                pass
            else:   
                for vote in votes:                    
                    other_list = vote["other_votes"]
                    if LazyLege.leg_id_in_list(other_list, key_lege_id):
                        #print("legid="+ key_lege_id + " bill_id=" + key_bill_id)
                        wimpy_bills_list.append(key_bill_id)
                    yes_list = vote["yes_votes"]
                    if LazyLege.leg_id_in_list(yes_list, key_lege_id):
                        #print("yes legid="+ key_lege_id + " bill_id=" + key_bill_id)
                        yes_bills_list.append(key_bill_id)
                    no_list = vote["no_votes"]
                    if LazyLege.leg_id_in_list(no_list, key_lege_id):
                        #print("no  legid="+ key_lege_id + " bill_id=" + key_bill_id)
                        no_bills_list.append(key_bill_id)
        return wimpy_bills_list, yes_bills_list, no_bills_list
    
    @staticmethod  
    def update_rascals_with_laziness(rascals, bills1):
        """
            build/update new attributes for each legislator
            that keeps track of the bills that werent voted on
            by this legislator
        """
        for key_lege_id, value_details in rascals.items():        
            wimped_bills, yes_bills, no_bills = LazyLege.find_wimpy_bills(bills1, key_lege_id)
            len_wim = len(wimped_bills)
            len_yes = len(yes_bills)
            len_no = len(no_bills)
            value_details["lazy_bills"] = wimped_bills
            value_details["lazy_count"] = len_wim
            value_details["yes_bills"] = yes_bills
            value_details["yes_count"] = len_yes 
            value_details["no_bills"] = no_bills
            value_details["no_count"] = len_no
            total_len = len_wim + len_yes + len_no
            value_details["total_count"] = total_len
            if total_len <= 0:
                fraction = 0.0
            else:
                fraction = float(len_wim) / float(total_len)
            value_details["lazy_fraction"] = fraction 
            #if len(wimped_bills) > 0:
            #    print("######")
        return
    
    @staticmethod
    def sort_rascals_by_laziness(rascals, maxnumber):
        """
        reverse sort legislators by "who skipped voting" the most
        and truncate so only the top "maxnumber" legislators are included
        in the output list
        """
        rascal_list = rascals.values()        
        rascals_by_laziness = sorted(rascal_list, key=lambda elem: elem['lazy_fraction'], reverse=True)
        rascals_by_laziness2 = rascals_by_laziness[:min(maxnumber, len(rascals_by_laziness))]
        return rascals_by_laziness2
  
    @staticmethod
    def get_lazy_rascals(maxnumber, rascal_dir_path, bills_dir_path):
        lege1 = lege.Lege()
        
        # get all the legislators and their attributes
        lege1.read_rascals_from_disk(rascal_dir_path)
        rascals_found = lege1.rascals
        
        # get the names of all the legislative sessions
        #session_List = bills.Bills.build_session_list()
        
        # get all the bills
        bills_found = bills.Bills.bill_files_to_dict_recursive(bills_dir_path)
        
        # some test code
        #for rascal in rascals_found.items():
            #wimpy_list = find_wimpy_bills(bills_found, rascal[0])
        
        # show bills not voted on for each legislator
        LazyLege.update_rascals_with_laziness(rascals_found, bills_found)
        
        # just show the most non-voting legislators
        sorted_rascals = LazyLege.sort_rascals_by_laziness(rascals_found, maxnumber)
        #print(sorted_rascals)
        
        return sorted_rascals
    
    @staticmethod
    def print_laziest_rascals(lazy_rascals):
        """
            print out a set of info about each legilator
        """
        for rascal in lazy_rascals:
            print(rascal["first_name"] + " " + rascal["last_name"] + " number missed votes: " + str(rascal["lazy_count"]) + " / " + str(rascal["total_count"]))
        return

    
# an example relative path for legislator info        
RASCAL_DIR_PATH_EXAMPLE = "data/2017-07-01-tx-json/legislators"
# an example relative path for bills info 
BILLS_EXAMPLE_PATH = "data/2017-07-01-tx-json/bills/tx/833/lower"

BILLS_DIR_PATH = "data\\2017-07-01-tx-json\\bills\\tx"

#lazy_rascals = LazyLege.get_lazy_rascals(10, RASCAL_DIR_PATH_EXAMPLE, BILLS_DIR_PATH)
#LazyLege.print_laziest_rascals(lazy_rascals)
    
    