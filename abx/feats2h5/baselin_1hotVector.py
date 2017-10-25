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
import pdb

def one_hot_baseline(input_path, out, frame_rate= 0.01):
   """
   frame_rate : sampling rate, typically 10 ms (or 0.01s)
   input_path : path to the dataset

   """
   
   name=os.path.basename(input_path)
   data=pd.read_table(input_path, sep="\t", header=0)
   phones=list(set(data["#phoneme"]))
   caption_group=data.groupby("#file")
                              
   for caption in caption_group.groups.keys():
       df=caption_group.get_group(caption)
       df.reset_index(inplace=True)      
       list_feats=[]
       R=np.empty(1)
       R[0]=frame_rate
       for i in range(len(df)): 
           on=df["onset"].iloc[i]
           off=df["offset"].iloc[i]
           nb_frame=int(np.floor_divide((off-on),R[0]))
           for ff in range(nb_frame): 
               one_hot=np.empty(len(phones))
               for jj in range(len(phones)):
                   try :
                       if df["#phoneme"][i]==phones[jj]:
                       #pdb.set_trace()
                           one_hot[jj]=1
                       else: 
                           one_hot[jj]=0 
                   except: 
                        pdb.set_trace()
               list_feats.append(one_hot)
       arr_feats = np.array(list_feats)
       directory=out + "/npy/"
       try:
           os.stat(directory)
       except:
           os.mkdir(directory)           
       np.save(directory + "/"+ df["file"][0], arr=arr_feats,  allow_pickle=False)          
               
          
        
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', help = "Path to the phoneme item file ")
    parser.add_argument('-o', '--out', help = "Output folder containing the npy files")
    parser.add_argument('-f', '--frame_rate', type= float, default=0.01, help = "Frame rate in second, default is 0.01 s")
    
    args = parser.parse_args()
    
    one_hot_baseline(args.input_path, args.out, args.frame_rate)
	


    
    
        
        

