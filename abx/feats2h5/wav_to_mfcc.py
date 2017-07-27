#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 19:56:51 2017

@author: rachine
"""

import os 
from os import listdir
from os.path import isfile, join
import csv
import speechcoco.speechcoco as sp
import glob
import generate_features


#########
# Paths:
#########

#wav_folder = '/pylon2/ci560op/odette/data/mscoco/val2014/wav'
#output = '/pylon2/ci560op/rachine/data/mscoco/val2014/mfcc'


#########
# Generate features:
#########

def make_features(wav_folder, output_folder):
	files = glob.glob(os.path.join(wav_folder, '*.wav'))
	generate_features.generate_all(files, os.path.join(output_folder,'mfcc.h5f'),os.path.join(output_folder, 'fb_mvn_stacked.h5f'))


if __name__=='__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('wav_folder', help = "Folder with .wav files")
	parser.add_argument('output_folder', help = "Output folder for h5f files")
	args = parser.parse_args()
	print("Start generating Features")
	print("Wav folder : " + args.wav_folder)
	print("Output folder : " + args.output_folder)	
	make_features(args.wav_folder, args.output_folder)
	


