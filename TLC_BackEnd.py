#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import PySimpleGUI as sg
import lightkurve as lk
import numpy as np
import pandas as pd
import os


# Lista todos os setores observados para o alvo especificado em 'Target'
def search(tic):
    sector_list = []
    search = lk.search_lightcurve(target=f'TIC {tic}', author='SPOC', exptime=120)
    for i in range(len(search)):
        sector_list.append(search.table['mission'][i][12:])
    return sector_list

# Faz o download dos setores selecionados na segunda janela para o alvo especificado em "Target"
def download_sectors(selected_sectors):
    try:
        os.mkdir('dat')
    except FileExistsError:
        pass
    try:
        for i in range(len(selected_sectors)):
            search_1 = lk.search_lightcurve(target=f'TIC {tic}', sector=selected_sectors[i], author='SPOC', exptime=120)
            lc = search_1.download().normalize().remove_outliers(sigma=3.5)
            time = lc.time.value
            flux = lc.flux.value
            data = pd.DataFrame(np.column_stack([time,flux]), columns=['Time', 'Flux'])
            save_file = data.to_csv(f'dat/{tic.zfill(10)}_{selected_sectors[i].zfill(3)}.dat', sep=' ', index=None, header=None)
        msg = sg.popup('Files saved successfully!')
        return msg
    except UnboundLocalError:
        alert = sg.popup_error('Invalid entry, check the information!')
        return alert

# Faz o download de todos os setores observados dos alvos especificados no arquivo (deve ser um arquivo .csv ou .txt)
def download_list_all(file_address):
    try:
        os.mkdir('dat')
    except FileExistsError:
        pass
    try:
        file = pd.read_csv(file_address, sep=';')
        id_list = file.TIC
        for i in range(len(id_list)):
            tic = id_list[i]
            search = lk.search_lightcurve(target=f'TIC {tic}', author='SPOC', exptime=120)
            for j in range(len(search)):
                sector = search.table['mission'][j][12:]
                lc = search[j].download().normalize().remove_outliers(sigma=3.5)
                time = lc.time.value
                flux = lc.flux.value
                data = pd.DataFrame(np.column_stack([time,flux]), columns=['Time', 'Flux'] )
                save_file = data.to_csv(f'dat/{str(tic).zfill(10)}_{str(sector).zfill(3)}.dat', sep=' ', index=None, header=None)
        msg = sg.popup('Files saved successfully!')
        return msg
    except FileNotFoundError:
        alert = sg.popup_error('Invalid entry, check the information!')
        return alert

# Faz o download dos setores dentro do range especificado em 'Start' e 'Final' para todos os alvos especificados no arquivo (deve ser um arquivo .csv ou .txt)
def download_list_sec(file_address, start_sec, final_sec):
    try:
        os.mkdir('dat')
    except FileExistsError:
        pass
    try:
        file = pd.read_csv(file_address, sep=';')
        id_list = file.TIC
        for i in range(len(id_list)):
            tic = id_list[i]
            search = lk.search_lightcurve(target=f'TIC {tic}', author='SPOC', exptime=120)
            for j in range(len(search)):
                sector = search.table['mission'][j][12:]
                if int(start_sec) < int(sector) < int(final_sec):
                    lc = search[j].download().normalize().remove_outliers(sigma=3.5)
                    time = lc.time.value
                    flux = lc.flux.value
                    data = pd.DataFrame(np.column_stack([time,flux]), columns=['Time', 'Flux'])
                    save_file = data.to_csv(f'dat/{str(tic).zfill(10)}_{str(sector).zfill(3)}.dat', sep=' ', index=None, header=None)
        msg = sg.popup('Files saved successfully!')
        return msg
    except ValueError:
        alert = sg.popup_error('Invalid entry, check the information!')
        return alert


# Faz o download de todos os setores concatenados em uma única LC (merged) para o alvo especificado em 'Target'
def download_merged(tic):
    try:
        os.mkdir('merged')
    except FileExistsError:
        pass
    try:
        search = lk.search_lightcurve(target=f'TIC {tic}', author='SPOC', exptime=120)
        lc = search.download_all().stitch().remove_outliers(sigma=3.5)
        time = lc.time.value
        flux = lc.flux.value
        data = pd.DataFrame(np.column_stack([time,flux]), columns=['Time', 'Flux'] )
        save_file = data.to_csv(f'merged/{str(tic).zfill(10)}_merged.dat', sep=' ', index=None, header=None)
        msg = sg.popup('Files saved successfully!')
        return msg
    except AttributeError:
        alert = sg.popup_error('Invalid entry, check the information!')
        return alert


# Faz o download de todos os setores concatenados em uma única LC (merged) para todos os alvos especificados no arquivo (deve ser um arquivo .csv ou .txt)
def download_merged_all(file_address):
    try:
        os.mkdir('merged')
    except FileExistsError:
        pass
    try:
        file = pd.read_csv(file_address, sep=';')
        id_list = file.TIC
        for i in range(len(id_list)):
            tic = id_list[i]
            search = lk.search_lightcurve(target=f'TIC {tic}', author='SPOC', exptime=120)
            lc = search.download_all().stitch().remove_outliers(sigma=3.5)
            time = lc.time.value
            flux = lc.flux.value
            data = pd.DataFrame(np.column_stack([time,flux]), columns=['Time', 'Flux'] )
            save_file = data.to_csv(f'merged/{str(tic).zfill(10)}_merged.dat', sep=' ', index=None, header=None)
        msg = sg.popup('Files saved successfully!')
        return msg
    except FileNotFoundError:
        alert = sg.popup_error('Invalid entry, check the information!')
        return alert

