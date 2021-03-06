#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:21:25 2017

@author: elinlarsen
"""

import os 
import argparse
import numpy as np


def npz_to_npy(path_npz):
    
    d=np.load(path_npz)
    
    directory = os.path.dirname(path_npz)+"/npy/"
    try:
        os.stat(directory)
    except:
        os.mkdir(directory) 
    
    for fi, feat in  d.items(): 
        np.save(file= directory + fi, arr=feat, allow_pickle=False)
        
        
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path_npz', help = " .npz files to convert into a folder containing npy files")
    args = parser.parse_args()
    npz_to_npy(args.path_npz)

