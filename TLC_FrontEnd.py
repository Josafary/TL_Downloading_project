#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PySimpleGUI as sg
import lightkurve as lk
import numpy as np
import pandas as pd
import os
from TLC_BackEnd import *

##########################
#   LAYOUT DAS JANELAS   #
##########################
def main_window():
    sg.theme('DarkGray1')
    init_directory = 'C:/'
    layout = [
        [sg.Text('Target:', font=('Cambria', 14)), sg.Input('', key='-TARGET_INPUT-', size=(51, 0)), sg.Button('Search', key='-SEARCH_BUTTON-', size=(12, 0))],
        [sg.HSeparator()],
        [sg.Text('List of targets:', font=('Cambria', 14)), sg.Input(key='-TARGET_FILE-'), 
         sg.FileBrowse(initial_folder=init_directory, file_types=[('Text Files', '*.txt'), ('CSV Files', '*.csv')], enable_events=True, size=(12, 0))],
        [sg.Radio('All sectors', 'sec', font=('Cambria', 14), key='-ALL_SECTORS_RAD-', default=True, enable_events=True)],
        [sg.Radio('Choose sectors range:', 'sec', font=('Cambria', 14), key='-SECTORS_RAD-', enable_events=True), sg.Text('Start:', font=('Cambria', 14)), 
         sg.Input('', key='-START_INPUT-', disabled=True, disabled_readonly_background_color='gray', size=(5, 0)), 
         sg.Text('Final:', font=('Cambria', 14)), sg.Input('', key='-FINAL_INPUT-', disabled=True, disabled_readonly_background_color='gray', size=(5, 0))],
        [sg.HSeparator()],
        [sg.Push(), sg.Checkbox('All Sectors (MERGED)', key='-MERGED-', font=('Cambria', 14)), sg.Push()],
        [sg.HSeparator()],
        [sg.Text('')],
        [sg.Push(), sg.Button('DOWNLOAD', key='-DOWNLOAD_BUTTON_1-', size=(12, 2)), sg.Push()]
    ]
    return sg.Window('TLC Download Project', layout=layout, size=(550, 300), finalize=True)

def sectors_window():
    sg.theme('DarkGray1')
    layout = [
        [sg.Push(), sg.Button('Download merged', key='-MERGED_BUTTON-'), sg.Push()],
        [sg.Text('Observed Sectors:', font=('Cambria', 14))],
        [sg.Push(), sg.Listbox(data, size=(5, 10), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key='-LIST-', enable_events=True), sg.Push()],
        [sg.Button('Download', key='-DOWNLOAD_BUTTON_2-'), sg.Push(), sg.Button('Cancel', key='-CANCEL_BUTTON-')]
              
    ]
    return sg.Window('List of Sectors', layout=layout, size=(250, 300), finalize=True)

############################
#   CRIAÇÃO DAS JANELAS   #
###########################
window_1, window_2 = main_window(), None

while True:
    window, event, values = sg.read_all_windows()
    
    if window == window_1 and event == sg.WIN_CLOSED:
        break
        
    elif window == window_1 and event == '-SEARCH_BUTTON-':
        tic = values['-TARGET_INPUT-']
        data = search(tic)
        window_2 = sectors_window()
        
    elif window == window_2 and event == '-DOWNLOAD_BUTTON_2-':
        selected_sectors = values['-LIST-']
        download_sectors(selected_sectors)
        
    
    elif window == window_2 and event == '-MERGED_BUTTON-':
        download_merged(tic)
        
    elif window == window_2 and event == sg.WIN_CLOSED:
        window_2.hide()
        
    elif window == window_2 and event == '-CANCEL_BUTTON-':
        window_2.hide()
        
    elif window == window_1 and values['-ALL_SECTORS_RAD-'] == True:
        window_1['-START_INPUT-'].update(disabled=True)
        window_1['-FINAL_INPUT-'].update(disabled=True)
        if event == '-DOWNLOAD_BUTTON_1-':
            if values['-MERGED-'] == False:
                file_address = values['-TARGET_FILE-']
                download_list_all(file_address)
            
            elif values['-MERGED-'] == True:
                file_address = values['-TARGET_FILE-']
                download_merged_all(file_address)
            
    elif window == window_1 and values['-SECTORS_RAD-'] == True:
        window_1['-START_INPUT-'].update(disabled=False)
        window_1['-FINAL_INPUT-'].update(disabled=False)
        if event == '-DOWNLOAD_BUTTON_1-':
            file_address = values['-TARGET_FILE-']
            start_sec = values['-START_INPUT-']
            final_sec = values['-FINAL_INPUT-']
            download_list_sec(file_address, start_sec, final_sec)
            

window.close()


# In[ ]:




