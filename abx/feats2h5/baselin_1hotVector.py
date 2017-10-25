#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:19:18 2017

@author: elinlarsen
"""

import numpy as np
import os
import pandas as pd
from os import listdir
import argparse

def one_hot_baseline(input_path, out, nb_to_sec=1, frame_rate= 0.01):
   """
   nb_to_sec : number to convert onset et offset in sec , default is 1
   frame_rate : sampling rate, typically 10 ms (or 0.01s)
   input_path : path to the dataset

   """
   
   name=os.path.basename(input_path)
   df=pd.read_table(input_path, sep=" ", header=0)
   
   #onset and offset are in 100* nanosecond. Need to be put in second
   
   df["onset"]=df["onset"]*nb_to_sec
   df["offset"]=df["offset"]*nb_to_sec   
   phones=list(set(df["#phoneme"]))
   list_feats=[]
   R=np.empty(1)
   R[0]=frame_rate
   for i in range(len(df)): 
       on=df["onset"].iloc[i]
       off=df["offset"].iloc[i]
       nb_frame=int(np.floor_divide((off-on),R[0]))
       for ff in range(nb_frame): 
           one_hot=np.empty(len(phones))
           for j in range(len(phones)):
               if df["phone"][i]==phones[j]:
                   one_hot[j]=1
               else: 
                   one_hot[j]=0
           list_feats.append(one_hot)
   arr_feats = np.array(list_feats)
   
   directory=out + "/npy/"
   try:
       os.stat(directory)
   except:
       os.mkdir(directory)
              
   np.save(directory + "/"+ name.split(".")[0], arr=arr_feats,  allow_pickle=False)          
               
          
        
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_folder_path', help = "Folder with features .lab files")
    parser.add_argument('-o', '--out', help = "Output folder containing the npy files")
    parser.add_argument('-n', '--nb_to_sec', type=int, default=1, help = "Output folder containing the npy files")
    parser.add_argument('-f', '--frame_rate', type= float, default=0.01, help = "Frame rate in second, default is 0.01 s")
    
    args = parser.parse_args()
    
    one_hot_baseline(args.input_path, args.out, args.nb_to_sec, args.frame_rate)
	


    
    
        
        

