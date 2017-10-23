#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 18:52:04 2017

@author: elinlarsen
"""

import os 
import numpy as np
import pandas as pd
import argparse
    
    
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
    
    sampled= df[df[col].isin(selected)]
    
    s=sampled[sampled['context'].str.contains("BREATH")==False]
    s=s[s['context'].str.contains("NOISE")==False]
    s=s[s['context'].str.contains("LAUGH")==False]
    s=s[s['context'].str.contains("HUMAN")==False]
    s=s[s['context'].str.contains("GARBAGE")==False]
    s=s[s['#phoneme'].str.contains("GARBAGE")==False]
    
    directory= os.path.dirname(item_file)

    s.to_csv(directory + "/sampled.item", sep="\t", header=True, index=False)
    
    return(s)
    


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
    
    df_sample.to_csv(output, sep="\t", header=True, index=False)
    
    return(df_sample)
   
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--item_file', help = "path containing the item file")
    parser.add_argument('-c', '--col', type= str, default= "#file", help= "name of the col to sample on")
    parser.add_argument('-s', '--sample_size', type=int, default= 1000, help="size of the sample : number of row to randomly select")
    parser.add_argument('-r', '--replace', type=bool, default='False', help = "whether or not to have a sampling with replacement")
    args = parser.parse_args()
    
    random_sampling(args.item_file, args.col, args.sample_size, args.replace)
    
    
