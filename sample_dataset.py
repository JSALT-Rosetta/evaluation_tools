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
    Randomly sample a list of file in a directory by choosing those that contain the desized speaker 
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
    
    #print("\n")
    #print( new_list)
    #randomly sample files names in the new list 
    sampled_files=np.random.choice(np.asarray(new_list),sample_size,replace)
    
    #save the list as an numpy array
    np.array(sampled_files).dump(open(os.path.join(new_path, 'name_sampled.npy'), 'wb'))
    
    #mv the the selected files to the new directory
    for file_name in sampled_files:
        full_file_name = os.path.join(input_path, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, new_path)
    
    

def get_sampled_files(input_path, new_path, sampled_wav_path, type_file):
    """
    Suppose that audio files have been sampled by the function  "sample_audio_files"
    Get image or json files corresponding to the audio sample
    ----------
    input_path : string, 
        directory path where files to sample are 
    new_path : string,
         name of of the path where will be the new sampled dataset
    sampled_wav_path : string,    
         path to the audio file sampled
    """
    
    new_list=[]
    
    #create a directory "subset_mscoco/img" or "subset_mscoco.json"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    #get into the directory containing images file to sample
    #load list containing name of files
    inputfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    print(inputfiles)
     
    #select files that have the same ID than in the audio sampled files
    wavfiles=[f for f in listdir(sampled_wav_path) if isfile(join(sampled_wav_path, f))]
    print(wavfiles)
    
    #get inputfiles that have a string in commun with wavfiles:
    for i1, i2 in getMatchingIndex(wavfiles, inputfiles):
        print(inputfiles[i2])
        new_list.append(inputfiles[i2]) 
        
    
    #save the list as an numpy array
    np.array(new_list).dump(open(os.path.join(new_path, 'name_sampled.npy'), 'wb'))
    print(new_list)
    #mv the the selected files to the new directory
    for file_name in new_list:
        full_file_name = os.path.join(input_path, file_name)
        try :
            (os.path.isfile(full_file_name))
            shutil.copy(full_file_name, new_path)
        except ValueError: 
            print("file name is invalid")
    



def getNum(image_name_list, type_file="image"):
    for s in image_name_list:
        s = s.split('_')[-1] # take the last string 
        s=s.split('.')[0] # get rid of the extension
        if type_file=="image":
            s=s.replace("000000","")# get rid of 0 
        yield s
            
            
            

def getMatchingIndex(list1, list2):
    for (i, num) in enumerate(getNum(list1)):
        if not num:
            continue
        for (j, other_num) in enumerate(getNum(list2)):
            if (num == other_num):
                yield (i, j)

   
    