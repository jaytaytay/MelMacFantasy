# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 12:14:42 2019

@author: hussl1
"""

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         Boke hvisualisation MM Fantasy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ==============================================================================
# Chapter 1: Import modules
# ==============================================================================

import pandas as pd
#import sys
import os
import datetime
import matplotlib.pyplot as plt
import calendar
import matplotlib as mpl
import numpy as np

import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.models import Range1d, HoverTool, ColumnDataSource, CategoricalColorMapper, Panel, CrosshairTool
from bokeh.models.widgets import CheckboxGroup
from bokeh.io import output_file, show, curdoc, show, push_notebook, output_notebook
from bokeh.layouts import WidgetBox, gridplot, layout, column, row 

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler

#from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs
#from bokeh.palettes import Category20_16


from dateutil.relativedelta import relativedelta
today_date = datetime.datetime.today()

import timeit
start = timeit.default_timer()

# =============================================================================
# Max Number from String Function
# =============================================================================
import re 
  
def extractMax(input): 
  
     # get a list of all numbers separated by  
     # lower case characters  
     # \d+ is a regular expression which means 
     # one or more digit 
     # output will be like ['100','564','365'] 
     numbers = re.findall('\d+',input) 
  
     # now we need to convert each number into integer 
     # int(string) converts string into integer 
     # we will map int() function onto all elements  
     # of numbers list 
     numbers = map(int,numbers) 
  
     return max(numbers) 
     
def remove_control_chart(s):
    return re.sub(r'\\x..', '', s)    
# =============================================================================
# Chapter 2: Files
# =============================================================================

filepath        = os.getcwd()
dirpath         = os.path.dirname(filepath)
dirdirpath      = os.path.dirname(dirpath)
dirdirdirpath   = os.path.dirname(dirdirpath)

outputpath      = os.path.join(dirpath, 'outputs', 'completion_time%s.png' % today_date.strftime("%Y-%m-%d %H" + 'h' + "%M" + 'm' + "%S" + 's'))
logpath         = os.path.join(dirpath, 'logs')
results_path    = os.path.join(filepath, 'MM Fantasy EPL 2018.xlsx')

df_raw      = pd.read_excel(results_path, header=None)

df_results = pd.DataFrame(columns=['Home_Team', 'Away_Team', 'Home_Player', 'Away_Player','Home_Score', 'Away_Score', 'Gameweek'])

# =============================================================================
# Chapter 3: Data Structuring
# =============================================================================


j=0
for i in range(0, len(df_raw)):
    if  "Gameweek" in df_raw.loc[i][0]:
        gameweek = extractMax(df_raw.loc[i][0])
    elif  "Next" in df_raw.loc[i][0]:
        pass
    else:
        df_results.loc[j] = [np.nan for n in range(df_results.shape[1])]
        
        df_results.loc[j]['Home_Team']      = df_raw.loc[i][0].split(', ')[0]
        df_results.loc[j]['Home_Player']    = df_raw.loc[i][0].split(', ')[1]
        df_results.loc[j]['Home_Score']     = df_raw.loc[i][1].split(' -')[0]
        df_results.loc[j]['Away_Score']     = df_raw.loc[i][1].split(' - ')[1]
        df_results.loc[j]['Away_Team']      = df_raw.loc[i][2].split(', ')[0]
        df_results.loc[j]['Away_Player']    = df_raw.loc[i][2].split(', ')[1]
        df_results.loc[j]['Gameweek']       = gameweek
        
        j+=1
     
 
df_single_lines = pd.DataFrame(columns=['Team', 'Opp_Team', 'Player', 'Opp_Player','Score', 'Opp_Score', 'Gameweek', 'Result'])

j=0
for i in range(0, len(df_results)):
    df_single_lines.loc[j] = [np.nan for n in range(df_single_lines.shape[1])]
    df_single_lines.loc[j]['Team']      = df_results.loc[i]['Home_Team']
    df_single_lines.loc[j]['Opp_Team']  = df_results.loc[i]['Away_Team']
    df_single_lines.loc[j]['Player']    = df_results.loc[i]['Home_Player']
    df_single_lines.loc[j]['Opp_Player']= df_results.loc[i]['Away_Player']
    df_single_lines.loc[j]['Score']     = df_results.loc[i]['Home_Score']
    df_single_lines.loc[j]['Opp_Score'] = df_results.loc[i]['Away_Score']
    df_single_lines.loc[j]['Gameweek']  = df_results.loc[i]['Gameweek']
    
    if df_results.loc[i]['Home_Score'] > df_results.loc[i]['Away_Score']:
        df_single_lines.loc[j]['Result']    = 'W'
    elif df_results.loc[i]['Home_Score'] < df_results.loc[i]['Away_Score']:
        df_single_lines.loc[j]['Result']    = 'L'
    else:
        df_single_lines.loc[j]['Result']    = 'D'
    
    j+=1
    
    df_single_lines.loc[j] = [np.nan for n in range(df_single_lines.shape[1])]
    df_single_lines.loc[j]['Team']      = df_results.loc[i]['Away_Team']
    df_single_lines.loc[j]['Opp_Team']  = df_results.loc[i]['Home_Team']
    df_single_lines.loc[j]['Player']    = df_results.loc[i]['Away_Player']
    df_single_lines.loc[j]['Opp_Player']= df_results.loc[i]['Home_Player']
    df_single_lines.loc[j]['Score']     = df_results.loc[i]['Away_Score']
    df_single_lines.loc[j]['Opp_Score'] = df_results.loc[i]['Home_Score']
    df_single_lines.loc[j]['Gameweek']  = df_results.loc[i]['Gameweek']
    
    if df_results.loc[i]['Home_Score'] < df_results.loc[i]['Away_Score']:
        df_single_lines.loc[j]['Result']    = 'W'
    elif df_results.loc[i]['Home_Score'] > df_results.loc[i]['Away_Score']:
        df_single_lines.loc[j]['Result']    = 'L'
    else:
        df_single_lines.loc[j]['Result']    = 'D'
        
    j+=1

# =============================================================================
# Chapter 4: PLots
    
# =============================================================================
    
colormap = {'L': 'red', 'W': 'green', 'D': 'blue'}
colors = [colormap[x] for x in df_single_lines['Result']]
df_single_lines['colors'] = colors

#sort to order legend as W-L-D
df_single_lines = df_single_lines.sort_values('Result', ascending = False)

# Dataset based on selected players
def make_dataset(player_list):

#    df_filter = pd.DataFrame(columns=['Team', 'Opp_Team', 'Player', 'Opp_Player','Score', 'Opp_Score', 'Gameweek', 'Result'])
    df_filter = df_single_lines
    df_filter['fill_alpha'] = 0.1
    df_filter['size'] = 6
    # Iterate through all the carriers
    if player_list == []:
        df_filter['fill_alpha'] = 1
        df_filter['size'] = 10
    else:
        for i in player_list:
            df_filter.loc[df_filter.Player == i, 'fill_alpha'] = 1
            df_filter.loc[df_filter.Player == i, 'size'] = 10
    return ColumnDataSource(df_filter)

# Styling for a plot
def style(p):
    # Title 
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.title.text_font = 'serif'

    # Axis titles
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_style = 'bold'

    # Tick labels
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'

    return p

# Function to make the plot
def make_plot(src):
    # Blank plot with correct labels
    p = figure(title="Mel McLaughlin Fantasy League 2018/19", 
               y_range=Range1d(0, 100, bounds="auto"),
               x_range=Range1d(0, 1+int(df_single_lines['Gameweek'].max()), bounds="auto"),
               plot_width=1500, plot_height=1000,
               x_axis_label = 'Game Week',
               y_axis_label = 'Points'
#               tooltips=TOOLTIPS
               )
    
    p.circle('Gameweek', 'Score', source=src, alpha='fill_alpha', size='size', color = 'colors', legend = 'Result')
    
    hover = HoverTool(tooltips=[('Week', '@Gameweek'),
                                ('Player', '@Player, @Team'),
                                ('Opposition', '@Opp_Player, @Opp_Team'),
                                ('Score', '@Score - @Opp_Score (@Result)'),
                                ])
    p.add_tools(hover)
    
    crosshair = CrosshairTool()
    p.add_tools(crosshair)
    
    p.legend.click_policy = 'hide'

    # Styling
    p = style(p)
    
    return p


# Update the plot based on selections
def update(attr, old, new):
    players_to_plot = [player_selection.labels[i] for i in player_selection.active]

    new_src = make_dataset(players_to_plot)

    src.data = new_src.data
#    source.data = new_src.data
    
players = list(set(df_single_lines['Player']))
player_selection = CheckboxGroup(labels= players, active=[])
player_selection.on_change('active', lambda attr, old, new: update())

# Find the initially selected players
#initial_players = players
initial_players = [player_selection.labels[i] for i in player_selection.active]

src = make_dataset(initial_players)

p = make_plot(src)

# Put controls in a single element
controls = WidgetBox(player_selection)

# Create a row layout
layout = row(p, controls)

#TOOLTIPS =
#"""
#    <div>
#        <div>
#            <span style="font-size: 17px; font-weight: bold;">@Player</span>
#            <span style="font-size: 15px; color: #966;">[$index]</span>
#        </div>
#        <div>
#            <span>@fonts{safe}</span>
#        </div>
#        <div>
#            <span style="font-size: 15px;">Location</span>
#            <span style="font-size: 10px; color: #696;">($x, $y)</span>
#        </div>
#    </div>
#"""


# show the results
#show(p)

#l = layout([
#[p],
#[w]], sizing_mode='stretch_both')


# show the results



#curdoc().add_root(layout)
show(layout)
reset_output()
output_file("Fantasy.html")


apps = {'/': Application(FunctionHandler(make_document))}

server = Server(apps, port=5000)
server.start()