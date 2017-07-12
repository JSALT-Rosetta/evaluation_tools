#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:08:40 2017

@author: elinlarsen
"""

import os 
import shutil
from os import listdir
from os.path import isfile, join
import numpy as np
from collections import Counter


def select_speaker_in_wav(input_path, speakers): 
    """
    Get all audio captions name file that are said by the selected speakers
    ----------
    """
    new_list=[]

    #get into the directory containing audio files to sample
    # and load list containing name of files
    onlyfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    #print(onlyfiles)
 
    #for each speaker selected, select files containing its name
    for sub in speakers:
        new_list.extend([s for s in onlyfiles if sub in s])
        
    return(new_list)
    

def get_nb_caption_per_img(n, selected_captions): 
    """
    Get image id from audio caption file namesthat were selected by their speakers
    Choose images that have at least n captions per image
    ----------
    n : int, 
        desired number of caption per image
    selected_captions : list of string, 
        list of caption file names selected by their speakers
    """
    
    counter_nb_caption=Counter()
    
    for cap in selected_captions: 
        #get image id 
        ImgID = cap.split('_')[-0]
        # add a count 
        counter_nb_caption[ImgID]+=1
        
    #choose img_id that have a count of n
    d=dict((k, v) for k, v in counter_nb_caption.items() if v == n)
    
    ImgID_selected=d.keys()
    
    return(ImgID_selected)
        


def cost_function(sampled_ImgIds, ImgID_selected, dict_nb_cat_per_img):
    sample_dict=dict((k, dict_nb_cat_per_img[k]) for k in sampled_ImgIds)
    
    freq_sample=[]
    freq_population=[]
    
    for key, value in sample_dict.items():
        freq_sample.append(len(value))
        
    for key, value in dict_nb_cat_per_img.items():
        freq_population.append(len(value))
    
    #cost function: 
        cost=freq_sample/freq_population
        
    return(cost)

    
    
def sample_img_id(dict_nb_cat_per_img, ImgID_selected, output_path, sample_size, T_0, T_fin, tau, nb_iter,  replace=False):
    """
    From the selected image id, sample them randomly in order to have 
    The sample size wanted and constraints respected
    ----------
    
    """
    
    ######## intialization ########    
    #randomly sample files names in the new list 
    sampled_ImgIds_0=np.random.choice(np.asarray(ImgID_selected),int(sample_size),replace)
    cost_0=cost_function(sampled_ImgIds_0, ImgID_selected, dict_nb_cat_per_img)
    
    i=0
    sample=sampled_ImgIds_0
    cost=cost_0
    T=T_0

    ######## algorithm MH ########
    while T > T_fin and cost<1 and i < nb_iter: 
        
        rest=[item for item in ImgID_selected if item not in sample]
        take_one_out=np.random.choice(np.asarray(sample),1,replace)
        new_sampled_ImgID=np.random.choice(np.asarray(rest),1,replace)
        
        # replace take_one_out by new_sampled_ImgID        
        new_sample=sample
        for index, item in sample.enumerate():
            if item==take_one_out: 
                new_sample[index]=new_sampled_ImgID
        
        
        new_cost=cost_function(new_sample, ImgID_selected, dict_nb_cat_per_img)
        
        if new_cost < cost: 
            cost=new_cost
            sample=new_sample
            
        else: 
            p=np.random.uniform(0, 1)
            if p < np.exp(-(new_cost-cost)/T):
                cost=new_cost
                sample=new_sample
            else: 
                pass
            
            
        T = T_0*(np.exp(-i/tau))
        i+=1
    
    return(sample)


