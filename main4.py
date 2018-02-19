"""
This script is used to generate and plot some simple
statistics based on texas legislator and bill data from 
Open States.  

I am currently using this to find the top 10 legislators
who skip voting the most.  I noted that many legislators
show up with many "other" (rather than yes or no) votes
in open states.  I figure that it would be interesting to
display the top offenders.  These votes may be all the way
from strategic non-votes to just not bothering to attend
parts of the session.  In any case, this prompts reasonable
questions that should be asked of the legislators before
they ask for any more votes from us.

The data can be obtained from https://openstates.org/

While open states provides an online api, this version relies on 
json files downloaded in bulk from open states.

Created on Wed Feb  7 14:08:23 2018

@author: jim grenadier
"""
#import os
#import json
#import lege
#import bills
import lazylege
import display

# an example relative path for legislator info        
RASCAL_DIR_PATH_EXAMPLE = "data/2017-07-01-tx-json/legislators"
# an example relative path for bills info 
BILLS_EXAMPLE_PATH = "data/2017-07-01-tx-json/bills/tx/833/lower"

BILLS_DIR_PATH = "data\\2017-07-01-tx-json\\bills\\tx"

# get the data from json files
lazy_rascals = lazylege.LazyLege.get_lazy_rascals(10, RASCAL_DIR_PATH_EXAMPLE, BILLS_DIR_PATH)

# print the top 10 legislators that had the most non-yes or no votes for testing
lazylege.LazyLege.print_laziest_rascals(lazy_rascals)

# display a barchart or the top 10 legislators that 
# had the most non-yes or no votes for testing
lege_display = display.Display(lazy_rascals) # not used yet
display.Display.plot_barchart(lazy_rascals)





