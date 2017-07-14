#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 18:52:04 2017

@author: elinlarsen
"""


import numpy as np
import pandas as pd
<<<<<<< HEAD
=======

>>>>>>> 208817fbca1bb0647e0c884a3e80e17b872652ae

    
    
def random_sampling(item_file, col, sample_size, replace=False):
    """
    Sample an item file to get a reasonable size for running an ABX task
    Parameters
    ----------
    item file : text file containing at least as columns :  onset, offset, 
    #phoneme and context and side information such as image ID
    col : string,
         name of one of a column of the item file to sample on
    sample_size : int,    
         number of values of 'col' to get from the sampling,
    replace: Bool,
         if True, the sampling will by replacement, default=False
    """
    
    #open item file
    df=pd.read_csv(item_file, sep='\t')
    
    #drop empty column
    try : 
        df.drop('Unnamed: 0', axis=1, inplace=True)
    except :
        pass
    
    #randomly sample the observations 
    try : 
        selected=np.random.choice(df[col],sample_size,replace)
    except ValueError:
        print ("The group_by value is not a colunm names of the item file")
    
    sampled_data = df[df[col].isin(selected)]
    
    return(sampled_data)
    

def get_sample_item_file(wav_file_names_sample, item_file, output):
    """
    From a sampled dataset, get an item file for running an ABX task
    Parameters
    ----------
    item file : text file containing at least as columns : #filename, onset, offset, 
    #phoneme and context and side information such as image ID
    item_file : string,
         path to the item file of the whole dataset
    output: string, 
        path where the sample item file will be stored
    """
    wav_names=[]
    temp=np.load(wav_file_names_sample)
    for s in temp:
        wav_names.append(s.split(".")[0])
    
    df=pd.read_csv(item_file, sep="\t", index_col="#filename")
    df_sample=df.loc[wav_names]
    
    df_sample.to_csv(output, sep="\t", header=True, index=True)
    
    return(df_sample)
    
