#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:08:40 2017

@author: elinlarsen
"""


from os import listdir
from os.path import isfile, join
import numpy as np
from collections import Counter
import scipy

import get_objects_categories
import pandas as pd



def select_speaker_in_wav(input_path, speakers): 
    """
    Get all audio captions name file that are said by the selected speakers
    ----------
    speakers: dictionnary of speaker id as keys and their probability to occur as value
    """
    new_list=[]

    #get into the directory containing audio files to sample
    # and load list containing name of files
    files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    
    df=pd.DataFrame(files, columns=["wave_files"])
    for sub in speakers:
        l=[sub for s in files if sub in s]
    df["speaker_id"]=l
    
    gp_spk=df.groupby("speaker_id")
    
    for spk, proba in speakers.items() : 
        
        df_spk=gp_spk.get_group(spk)
        selected_spk=df_spk.sample(frac=proba, replace=False, weights=None, axis=0)
        if spk==speakers.items()[0]:
            final_df=selected_spk
        else: 
            final_df=pd.concat([final_df, selected_spk], axis=0)

        
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
        


def cost_function(sampled_ImgIds, ImgID_selected, dic_ImgID_to_cat_pop):
    """
    Calculate a cost function which is Chi square test 
    For each object category, get the number of image in which the category is present
    in the sample and in the population. 
    Compare the two distribution. 
    ----------
    
    """
    
    ### get the number of images containing an object category for each category 
    #in the population dataset
    dic_cat_to_ImgID_pop=get_objects_categories.reverse_dic(dic_ImgID_to_cat_pop, save=False, name="") 
    Nb_cat=len(dic_cat_to_ImgID_pop)
    freq_pop=get_objects_categories.dict_nb_value_per_key(dic_cat_to_ImgID_pop, show_plot=False)
    Nb_Img_per_cat_pop=np.array(freq_pop.items())
    
    
    ### get the dictionary from image ID to category for the selected image ID
    
    sample_dict=dict((int(k), dic_ImgID_to_cat_pop[int(k)]) for k in sampled_ImgIds)
    dic_cat_to_ImgID_sample=get_objects_categories.reverse_dic(sample_dict, save=False, name="")

    
    ### get the number of images containing an object category for each category 
    #in the sampled dataset
    freq_sample=get_objects_categories.dict_nb_value_per_key(dic_cat_to_ImgID_sample, show_plot=False)
    Nb_Img_per_cat_sample=np.array(freq_sample.items())
    
    cost=scipy.stats.chisquare(Nb_Img_per_cat_sample,Nb_Img_per_cat_pop, ddof=Nb_cat)
        
    return(cost)

    
    
def sample_img_id(dic_ImgID_to_cat_pop, ImgID_selected, output_path, sample_size, MH_sampling=False, T_0=100, T_fin=1, tau=2, nb_iter=100,  replace=False):
    """
    From the selected image id, sample them randomly in order to have 
    The sample size wanted and constraints respected
    ----------
    
    """
    
    ######## intialization ########    
    #randomly sample files names in the new list 
    sampled_ImgIds_0=np.random.choice(np.asarray(ImgID_selected),int(sample_size),replace)
    
    if MH_sampling:
        cost_0=cost_function(sampled_ImgIds_0, ImgID_selected, dic_ImgID_to_cat_pop)
        
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
            
            
            new_cost=cost_function(new_sample, ImgID_selected, dic_ImgID_to_cat_pop)
            
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
            print ("_".join("iteration", str(i)))
            
        return(sample)
    
    else: 
        return(sampled_ImgIds_0)
    
    

def get_Img_file_name_from_ID(ImgId_file, pre_name="COCO_", train=True, output_path=""):
    Img_file_name_list=[]
    #ImgID_list=np.load(ImgId_file)
    for ii in ImgId_file:
        fig=str(str(ii).zfill(12))
        if train: 
            Img_file_name_list.append(pre_name+ "train_2014_"+ fig +".jpg")
        else: 
            Img_file_name_list.append(pre_name+ "val_2014_"+ fig +".jpg")
    
    if output_path!="": 
        np.array(Img_file_name_list).dump(open(output_path+"/"+'Img_file_name.npy', 'wb'))
        
    return(Img_file_name_list)

    
def get_wav_file_name_from_ImgID(ImgId_file, wav_file_path, output_path=""):
    wav_files_name = [f for f in listdir(wav_file_path) if isfile(join(wav_file_path, f))]  
        
    for ImgID in ImgId_file:
        inter=[s for s in wav_files_name if ImgID in s]
        
    try: 
        thefile = open(output_path+'/wave_file_names.txt', 'w')
        for item in inter:
            thefile.write("%s\n" % item)
        thefile.close()
    except: 
        pass
    
    return(inter)


    for f in inter: 
        open(f, 'a').close()
    #if output_path!="": 
        #np.array(inter).dump(open(output_path+"/"+'wav_file_name.npy', 'wb')) 
    return(inter)
        
'''
    for w in wav_files_name: 
        for ii in ImgId_file:
             img_id= w.split('_')[0]
             if img_id==ii: 
                 wav_files_sample.append(w)
'''