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
import pdb


#########
# Paths:
#########

#feats_folder = '/pylon5/ci560op/londel/flickr/ploop_u100_s3_c4/posteriors_ac0.2/test/'
#output_folder = '/pylon5/ci560op/larsene/abx/flickr/posteriogram/test/'


def h5features_from_nparray(input_path, h5f, timefunc=None):
    """Compute speech features (such as posteriogram) that are in numpy array 
    in h5features format.

    Parameters:
    ----------
    input_path: path of the directory containing the features of audio files in numpy array
    h5f: str. Name of the h5features file to create.
    timefunc: callable. Function that returns timestamps for the aforementionned
        features. By default, it assume a window length of 25 ms and a window
        step of 10 ms.
        
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
        internal_files.append(os.path.basename(os.path.splitext(f)[0]))
    if features:
        h5features.write(h5f, "/features/", internal_files, times, features)


#########
# Generate features:
#########

def make_h5file(feats_folder, output_folder, name='posteriors'):
    h5features_from_nparray(feats_folder, os.path.join(output_folder,name +'.h5f'), timefunc=None)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--feats_folder', help = "Folder with features .npy files")
    parser.add_argument('-o', '--output_folder', help = "Output folder for h5f files")
    parser.add_argument('-n', '--name', default='posteriors', help = "Folder with .wav files")
    args = parser.parse_args()
    print("Start generating Features")
    print("Input folder : " + args.feats_folder)
    print("Output folder : " + args.output_folder)	
    
    make_h5file(args.feats_folder, args.output_folder, args.name)
	


