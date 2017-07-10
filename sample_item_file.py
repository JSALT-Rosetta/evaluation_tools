#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 18:52:04 2017

@author: elinlarsen
"""


import numpy as np
import pandas as pd


    
    
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
    
