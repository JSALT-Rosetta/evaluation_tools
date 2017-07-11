#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 13:44:04 2017

@author: elinlarsen
"""

import os 
import shutil
from os import listdir
from os.path import isfile, join
import numpy as np


def sample_audio_files(input_path, new_path, sample_size,  speakers, replace=False):
    """
    Randomly sample a list of wav file in a directory by choosing those that contain the desized speaker 
    Store numpy arrays of list of the selected wav file names and json file names
    ----------
    input_path : string, 
        directory path where files to sample are 
    new_path : string,
         name of of the path where will be the new sampled dataset
    sample_size : int,    
         number of files to select
    speakers: list of strings,
        name of speakers to include in the subset
    replace: Bool,
         if True, the sampling will by replacement, default=False
    """
    
    new_list=[]
    
    #create a directory "subset_mscoco/wav/"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    
    #get into the directory containing audio files to sample
    # and load list containing name of files
    onlyfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    #print(onlyfiles)
 
    #for each speaker selected, select files containing its name
    for sub in speakers:
        new_list.extend([s for s in onlyfiles if sub in s])
    
    #randomly sample files names in the new list 
    sampled_files=np.random.choice(np.asarray(new_list),int(sample_size),replace)
    
    #change wav extension into json extension
    json_files=[]
    for ss in sampled_files: 
        json_files.append(os.path.splitext(ss)[0]+".json")
    
    # use  jsonToSQL to create a sqlite3 database in the new directory with the selected files
    
    #save the list as an numpy array
    np.save(os.path.join(new_path, 'wav_file_name_sampled.npy'), sampled_files, allow_pickle=False)
    np.save(os.path.join(new_path, 'json_file_name_sampled.npy'), json_files, allow_pickle=False)
    
    #np.array(sampled_files).dump(open(os.path.join(new_path, 'wav_file_name_sampled.npy'), 'wb'))
    #np.array(json_files).dump(open(os.path.join(new_path, 'json_file_name_sampled.npy'), 'wb'))
    
    return(sampled_files)
    
    #mv the the selected files to the new directory
    '''
    for file_name in sampled_files:
        input_full_file_name = os.path.join(input_path, file_name)
        output_full_file_name = os.path.join(new_path, file_name)
        os.system ("cp input_full_file_name output_full_file_name")
        #if (os.path.isfile(full_file_name)):
            #shutil.copy(full_file_name, new_path)
    '''
    

def get_sampled_files(input_path, new_path, sampled_wav_path, type_file):
    """
    Suppose that audio files have been sampled by the function  "sample_audio_files"
    and their file names stored in a np array format
    Get image or json or vgg files corresponding to the audio sample
    ----------
    input_path : string, 
        directory path where files to sample are 
    new_path : string,
         name of of the path where will be the new sampled dataset
    sampled_wav_path : string,    
         path to the array file containing the sampled name files

    """
    
    #create a directory "subset_mscoco/img" or "subset_mscoco.json"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    #get into the directory containing images file to sample
    #load list containing name of files
    inputfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    
    #get dictionary with images file names and image ID
    dict_image=getImgID_jpg_or_json(inputfiles, type_file="image")
     
    #select files that have the same ID than in the audio sampled files
    wavfiles_names=np.load(sampled_wav_path)
    #wavfiles=[f for f in listdir(sampled_wav_path) if isfile(join(sampled_wav_path, f))]
    
    #get dictionary with images file names and image ID
    dict_wav=getImgID_wav(wavfiles_names)
    
    new_list=getMatchingKey1(dict_image, dict_wav)
    
    #save the list as an numpy array
    np.save(os.path.join(new_path, type_file+"_file_name_sampled.npy"), np.asarray(new_list), allow_pickel=False)
    
    #mv the the selected files to the new directory
    for file_name in new_list:
        full_file_name = os.path.join(input_path, file_name)
        try :
            (os.path.isfile(full_file_name))
            shutil.copy(full_file_name, new_path)
        except ValueError: 
            print("file name is invalid")
    


def getImgID_wav(wav_name_list):
    dictionary = {}
    for key in wav_name_list: 
        value = key.split('_')[0]
        dictionary[key]=value
    return(dictionary)
        

def getImgID_jpg_or_json(image_name_list, type_file="image"):
    dictionary = {}
    for s in image_name_list:
        v = s.split('_')[-1] # take the last string 
        v=v.split('.')[0] # get rid of the extension
        if type_file=="image":
            v=v.replace("000000","")# get rid of 0 
        dictionary[s]=v
    return(dictionary)
            
                     

def getMatchingKey1(dic1, dic2):
    t=[]
    for (k1, v1) in dic1.items():
        for (k2,v2) in dic2.items():
            if v1==v2:
                t.append(k1)
    return(t)
            
   
    
