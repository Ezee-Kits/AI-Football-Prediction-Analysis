from datetime import date, timedelta
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import requests
import random
import time
import os




def main_date(day):
    last_date = date.today() + timedelta(day)
    return last_date


def save_daily_csv(dir,date_num):
    outcome_dir = dir
    todays_dir = str(main_date(date_num))+' Files'
    full_path = os.path.join(outcome_dir,todays_dir)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path
    

def requests_init(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content,"html.parser")
    tree = html.fromstring(res.content)
    return soup,tree


def requesting_init(url,**kwargs):
    res = requests.get(url)


def bs4_init(url):
    soup = BeautifulSoup(url,'html.parser')
    return soup


def tree_init(optional):
    tree = html.fromstring(optional)


def saving_files(data,path):
    df = pd.DataFrame(data)
    print(df.to_string())

    try:
        df2 = pd.read_csv(path)
        all_df = pd.concat([df2, df], ignore_index=True)
        all_df.to_csv(path, index=False)
        print(' ------------------------------------ ALL FILES SAVED  ------------------------------------- \n \n')

    except:
        df.to_csv(path, index=False)
        print('============================= SECOND FILE SAVED ==========================')



def drop_duplicate(path):
    all_df = pd.read_csv(path)
    all_df = all_df.drop_duplicates(keep='first')
    all_df = all_df.reset_index()
    all_df.drop(['index'], axis=1, inplace=True)
    all_df.to_csv(path, index=False)


def drop_similar(path,val1,val2):
    df = pd.read_csv(path)
    drop_index = []
    for i,x in enumerate(df[val1]) :
        if df[val1][i] == df[val2][i]:
            drop_index.append(i)

    df.drop(drop_index, axis=0, inplace=True)
    df = df.reset_index()
    df.drop(['index'], axis=1, inplace=True)
    df.to_csv(path, index=False)

def drop_col(path,val):
    df = pd.read_csv(path)
    df.drop(val, axis=1, inplace=True)
    df = df.reset_index()
    df.drop(['index'], axis=1, inplace=True)
    df.to_csv(path, index=False)


def sorting_values(path,value,path_to_save,ascending_mode):
    df = pd.read_csv(path)
    df = df.sort_values(by=value,ascending=ascending_mode)
    df.to_csv(path_to_save, index=False)



def new_col_with2_vals(path,new_col_name,val1,val2):
    df = pd.read_csv(path)
    new_data = []
    for i,x in enumerate(df[df.columns[0]]):
        new_data.append( df[val1][i] + df[val2][i] )
    df[new_col_name] = new_data
    df.to_csv(path, index=False)

