#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 16:24:54 2017

@author: elinlarsen
"""


import numpy as np
import os
import pandas as pd
import math
from os import listdir
import argparse

def lab2npy(input_path, out, frame_rate= 0.01):
   """
   frame_rate : sampling rate, typically 10 ms (or 0.01s)

   """
   
   name=os.path.basename(input_path)
   df=pd.read_table(input_path, sep=" ", header=None)
   df.columns=["onset", "offset", "phone", "score"]
   
   #onset and offset are in 100* nanosecond. Need to be put in second
   
   df["onset"]=df["onset"]*10**(-7)
   df["offset"]=df["offset"]*10**(-7)   
   phones=['a{}'.format(i) for i in range(1, 49)]   
   list_feats=[]
   for i in range(len(df)): 
       on=df["onset"].iloc[i]
       off=df["offset"].iloc[i]
       nb_frame=math.floor((off-on)/frame_rate)
       for ff in range(nb_frame): 
           one_hot=np.empty(len(phones))
           for j in range(len(phones)):
               if df["phone"][i]==phones[j]:
                   one_hot[j]=1
               else: 
                   one_hot[j]=0
           list_feats.append(one_hot)
   arr_feats = np.array(list_feats)
   np.save(file=out + "/"+ name, arr=arr_feats,  allow_pickle=False)          
               
   

def make_npyfiles(input_folder_path,  out, frame_rate,):
   filenames = [f for f in listdir(input_folder_path) if os.path.splitext(f)[-1]==".lab"]
   for f in filenames:
       lab2npy(f, out, frame_rate,)
        
        
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_folder_path', help = "Folder with features .lab files")
    parser.add_argument('-o', '--out', help = "Output folder containing the npy files")
    parser.add_argument('-f', '--frame_rate', default='0.01', help = "Frame rate in second, default is 0.01 s")
    
    args = parser.parse_args()
    
    make_npyfiles(args.input_folder_path, args.out, args.frame_rate)
	


    
    
        
        

