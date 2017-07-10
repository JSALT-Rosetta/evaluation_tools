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
 
    #for each speaker selected, select files containing its name
    for sub in speakers:
        new_list.extend([s for s in onlyfiles if sub in s])
    

    #randomly sample files names in the new list 
    sampled_files=np.random.choice(new_list,sample_size,replace)
    
    #mv the the selected files to the new directory
    for file_name in sampled_files:
        full_file_name = os.path.join(input_path, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, new_path)
    
    

def get_sampled_files(new_path, input_path, sampled_wav_path, dataset="training"):
    
    new_list=[]
    
    #create a directory "subset_mscoco/img" or "subset_mscoco.json"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    #get into the directory containing images file to sample
    #load list containing name of files
    inputfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    
    
    #select files that have the same ID than in the audio sampled files
    wavfiles=[f for f in listdir(sampled_wav_path) if isfile(join(sampled_wav_path, f))]
    
    #get files in input_path that have 
    match=[]
    for w in wavfiles: 
        for ii in inputfiles:
            match.append()
    
    #attach match to a new list
    for m in match : 
        new_list.extend([s for s in inputfiles if m in s])
             
    #mv the the selected files to the new directory
    for file_name in match:
        full_file_name = os.path.join(input_path, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, new_path)
    
    
    