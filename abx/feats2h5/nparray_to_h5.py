#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:13:17 2017

@author: elinlarsen, rriad, bootphon team
"""

import os 
import argparse
from os import listdir
import numpy as np
import h5features
import pickle



def change_filename(inpath, file_newnames):
    with open (file_newnames, 'r') as f:
        newnames=f.readlines()
    newnames=[x.strip()+".npy" for x in newnames ] 
    old=[f for f in listdir(inpath)if os.path.splitext(f)[-1]==".npy"]
    sorted_old=sorted(old, key=lambda x: int(x.split(".")[0].split("_")[-1]))    
    for n,o in zip(newnames, sorted_old):
        os.rename(inpath+"/"+o, inpath+"/"+n)
    return(newnames)
    

def from_xnmt_format_to_filename(emb, output_dir, file_newnames):
    data = pickle.load(open(emb,'rb'))
    with open (file_newnames, 'r') as f:
        newnames=f.readlines()
    newnames=[x.strip()+".npy" for x in newnames ] 
    for d, f in zip(data, newnames):
        t=data.T
        np.save(file=output_dir +"/"+f, arr=t, allow_pickle=False)
        

def time_l2_CNN_Glass16(data):
    """
    time in second
    """
    time=np.arange(data.shape[0], dtype=float) * 0.02 + 0.015
    return(time)
    


    
def time_l3_CNN_Glass16(data):
    time=np.arange(data.shape[0], dtype=float) * 0.04 + 0.045
    return(time)




def h5features_from_nparray(input_path, h5f, timefunc=None, rm_last_number=False, transpose=False):
    """Compute speech features (such as posteriogram) that are in numpy array 
    in h5features format.

    Parameters:
    ----------
    input_path: path of the directory containing the features of audio files in numpy array
    h5f: str. Name of the h5features file to create.
    timefunc: callable. Function that returns timestamps for the aforementionned
        features. By default, it assume a window length of 25 ms and a window
        step of 10 ms.
    rm_last_number :bool, wether or not to remove the last number in each file name
    (the filenames of posteriograms have an additional number compared to the audio filenames )  
    """
    filenames = [f for f in listdir(input_path) if os.path.splitext(f)[-1]==".npy"]
    batch_size = 500
    features = []
    times = []
    internal_files = []
    i = 0
    for f in filenames:
        data=np.load(input_path+f)
        if i == batch_size:
            h5features.write(h5f, "/features/", internal_files, times,features)
            features = []
            times = []
            internal_files = []
            i = 0
        i = i+1
        features.append(data)
        if timefunc == None:
            time = np.arange(data.shape[0], dtype=float) * 0.01 + 0.0025
        else:
            time = timefunc(data)
        times.append(time)
        if rm_last_number:
            name=os.path.splitext(f)[0]
            internal_files.append(os.path.basename(name))
        else:
            internal_files.append(os.path.basename(os.path.splitext(f)[0]))
    if features:
        h5features.write(h5f, "/features/", internal_files, times, features)


#########
# Generate features:
#########

def make_h5file(feats_folder, output_folder, name, rm_last_number, transpose, xnmt_format=False, file_newnames=''):
    if xnmt_format==True:
        from_xnmt_format_to_filename(feats_folder, file_newnames)   
    h5features_from_nparray(feats_folder, os.path.join(output_folder,name +'.h5f'), None, rm_last_number, transpose)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--feats_folder', help = "Folder with features .npy files")
    parser.add_argument('-o', '--output_folder', help = "Output folder for h5f files")
    parser.add_argument('-n', '--name', default='posteriors', help = "Folder with .wav files")
    parser.add_argument('-t', '--timefunc', default=None, 
                        help = "function giving the time step between frame and the offset")
    parser.add_argument('-rm', '--rm_last_number', type=bool, default='False', 
                        help = "either or not to remove the last number in each file name separated by _")

    args = parser.parse_args()
    print("Start generating Features")
    print("Input folder : " + args.feats_folder)
    print("Output folder : " + args.output_folder)	
    
    make_h5file(args.feats_folder, args.output_folder, args.name, args.timefunc, args.rm_last_number)
	


