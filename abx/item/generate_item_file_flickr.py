# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:30:12 2017

@author: doctor
"""

"""
Generating an item file for the ABX task on Flickr 8K
"""

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from collections import defaultdict

path_labels='/pylon2/ci560op/odette/data/flickr/flickr_labels/'
df=pd.read_table("df_wav_spk_set.txt", sep='\t', header=0)
df["#file"]=[s.split('.')[0] for s in df["wave_file"]]
dataset_type="test"


def create_list_from_files_in_folder(input_path): 
    files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    return(files)



def get_wavname_from_alignment(path_alignement):
    
    align_filename= create_list_from_files_in_folder(path_alignement)
    wavname=[('_'.join(f.split("_")[1:])).split(".")[0] for f in align_filename]
    return(wavname)


def phone_to_triphone_alignment(df):
    """
    df dataframe must have as columns onset and offset of phonemes
    The function returns a dataframe with colunms of onset and offset of triphones
    """
    triphones_onset=[]
    triphones_offset=[]
    onset=df['onset']
    offset=df['offset']
    new_df=df
    for i in range(len(df)):
        if i==0:
            triphones_onset.append(onset[i])
        else:
            triphones_onset.append(onset[i-1])
            
        if i!=len(df)-1:
            triphones_offset.append(offset[i+1])
        else:
            triphones_offset.append(offset[i])
    new_df['onset']=triphones_onset
    new_df['offset']=triphones_offset
    return(new_df)


def dic_alignment_to_wave(path_alignement):  
    dic={}
    align_filename= create_list_from_files_in_folder(path_alignement)
    wavname=[('_'.join(f.split("_")[1:])).split(".")[0] for f in align_filename]
    for i in range(len(align_filename)):
        dic[align_filename[i]]= wavname[i] 
    return(dic)



def reverse_dic(dic, save=False, name=""):
    """
    For a given dictionary (dic), reverse keys and values. Return a dictionary
    """
    d = defaultdict(set)   
    for k in dic.keys(): 
        for v in dic.values():
            for ii in v: 
                d[ii].add(k)     
    if save: 
        with open(name, 'w') as fp:
            json.dump(d, fp)
    return(d)



def get_item_file(path_alignment, dataset_type, path_wav_spk_datasetype ):    
    dic=dic_alignment_to_wave(path_alignment)
    dic_rev=reverse_dic(dic, save=False, name="")
    df=pd.read_table(path_wav_spk_datasetype, sep='\t', header=0)  
    df["#file"]=[f.split(".")[0] for f in df["wave_file"]] # get rid of extension in file name
    df_set=df[df['dataset']==dataset_type] # subset the dataset to the set (train, dev or test)
    selected_align=[]  
    alignfiles= [v for k,v in dic.items()]
    wav_set=len(set(alignfiles).intersection(set(df_set['#file'])))
    for w in wav_set:
        selected_align.append(dic_rev(w))
    df_align=pd.DataFrame()
    for filename in selected_align:
        d=pd.read_table(path_alignment+filename, header=None, sep=" ", names=['#phoneme', 'onset', 'offset'])
        cols = d.columns.tolist()
        cols = cols[1:]+cols[0:1]
        d = d[cols] 
        df_filename=pd.DataFrame(np.repeat(dic[filename], len(d)), columns=['#file'])
        dd=pd.concat([df_filename, d], axis=1)
        df_align=pd.concat([df_align, dd], axis=0)    
    triphone_align=phone_to_triphone_alignment(df_align)    
    final=pd.merge(triphone_align, df_set, on='#file', how="inner")
    return(final)

def create_phonetic_context(df):
    """
    From a dataframe containing a colunms of phones, create another column 
    containing previous and following phones for each phone
    """
    context=[]
    phonemes=df["#phoneme"]
    for i in range(len(df)):
    
        context.append()