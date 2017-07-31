#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:13:17 2017

@author: elinlarsen
"""

import os 
import generate_features
import argparse
from os import listdir
from os.path import isfile, join
import numpy as np
import h5features


#########
# Paths:
#########

#feats_folder = '/pylon5/ci560op/londel/flickr/ploop_u100_s3_c4/posteriors_ac0.2/test/'
#output_folder = '/pylon2/ci560op/rachine/data/mscoco/val2014/mfcc'


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
    files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    batch_size = 500
    features = []
    times = []
    internal_files = []
    i = 0
    for f in files:
        if i == batch_size:
            h5features.write(h5f, '/features/', internal_files, times,
                             features)
            features = []
            times = []
            internal_files = []
            i = 0
        i = i+1
        features.append(f)
        if timefunc == None:
            time = np.arange(f.shape[0], dtype=float) * 0.01 + 0.0025
        else:
            time = timefunc(f)
        times.append(time)
        internal_files.append(os.path.basename(os.path.splitext(f)[0]))
    if features:
        h5features.write(h5f, '/features/',
                         internal_files, times,
                         features)


#########
# Generate features:
#########

def make_h5file(feats_folder, output_folder, name='posteriors'):
    generate_features.h5features_from_nparray(feats_folder, os.path.join(output_folder,name, 'h5f'), timefunc=None)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--feats_folder', help = "Folder with .wav files")
    parser.add_argument('-o', '--output_folder', help = "Output folder for h5f files")
    parser.add_argument('-n', '--name', default='posteriors', help = "Folder with .wav files")
    args = parser.parse_args()
    print("Start generating Features")
    print("Input folder : " + args.feats_folder)
    print("Output folder : " + args.output_folder)	
    
    make_h5file(args.feats_folder, args.output_folder, args.name)
	


