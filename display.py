# -*- coding: utf-8 -*-
"""
class to display statistics about legislative activity

Created on Sun Feb 18 18:39:54 2018

@author: jim grenadier
"""

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import GnBu3, OrRd3
from bokeh.plotting import figure
from bokeh.io import output_notebook

import lege

class Display(lege.Lege):

    def __init__(self, leg):
        """
        constructor not used much yet. 
        notes:
        After some refactoring, we will probably use it alot.
        """
        _rascals = leg
        return        

    @staticmethod    
    def build_lazy_name_list(lazy_rascals):
        """
        build names of legislators for in a format for displaying
        """
        just_names = list()
        for rascal in lazy_rascals:
            nom = rascal["first_name"] + " " + rascal["last_name"]
            just_names.append(nom)
        return just_names

    @staticmethod
    def build_value_list(lazy_rascals, dict_key):
        """
        utility method to extract a simple list of an attribute of a legislator.
        This is used to get data in a format that is easly usable by the 
        barchart.
        """
        just_values = list()
        for rascal in lazy_rascals:
            val = rascal[dict_key]
            just_values.append(val)
        return just_values
    
    @staticmethod
    def pct(in_list, just_total):
        """
            convert to percentage while copying the counts of the votes 
        """
        output_list = list()
        i = 0
        for v in in_list:
            output_list.append((v / just_total[i]) * 100.0)
            i = i + 1
        return output_list

    @staticmethod
    def plot_barchart(lazy_rascals):
        """
        plot a barchart of the percentage of votes cast for yes, no and other
        """
        output_file("bars.html")
        
        #
        # prepare the data in a format that the barchart likes
        just_names = Display.build_lazy_name_list(lazy_rascals)
        just_lazy = Display.build_value_list(lazy_rascals, "lazy_count")
        just_total = Display.build_value_list(lazy_rascals, "total_count")
        just_yes = Display.build_value_list(lazy_rascals, "yes_count")
        just_no = Display.build_value_list(lazy_rascals, "no_count")

        just_non_lazy = list()
        i = 0
        for val in just_total:
            just_non_lazy.append(val - just_lazy[0])
            i = i + 1
            
        output_file("bar_stacked_split.html")

        vote_types = ["other", "yes", "no"]

        vote_ds = dict()
        vote_ds["names"] = just_names
        vote_ds["no"] = Display.pct(just_no, just_total)
        vote_ds["yes"] = Display.pct(just_yes, just_total)
        vote_ds["other"] = Display.pct(just_lazy, just_total)

        p = figure(y_range=just_names, plot_height=350, x_range=(0, 100), title='Texas legislators with most percent "other" votes',
                   toolbar_location="right")

        p.hbar_stack(vote_types, y='names', height=0.5, color=GnBu3, source=ColumnDataSource(vote_ds),
                     legend=["%s votes" % x for x in vote_types])

        p.y_range.range_padding = 0.2
        p.ygrid.grid_line_color = None
        p.legend.location = "center"
        p.axis.minor_tick_line_color = None
        p.outline_line_color = "Black"
        show(p)      
        return
            