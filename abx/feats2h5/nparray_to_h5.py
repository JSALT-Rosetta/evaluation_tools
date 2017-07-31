#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:13:17 2017

@author: elinlarsen
"""

import os 
import generate_features


#########
# Paths:
#########

#feats_folder = '/pylon5/ci560op/londel/flickr/ploop_u100_s3_c4/posteriors_ac0.2/test/'
#output_folder = '/pylon2/ci560op/rachine/data/mscoco/val2014/mfcc'



#########
# Generate features:
#########

def make_h5file(feats_folder, output_folder, name='posteriors'):
	generate_features.generate_all(files, os.path.join(output_folder,'mfcc.h5f'),os.path.join(output_folder, 'fb_mvn_stacked.h5f'))
       generate_all(files, alignement_h5f, input_h5f,
                 nframes=7, vad=None)
      h5features_from_nparray(feats_folder, os.path.join(output_folder,name, 'h5f'), timefunc=None)

if __name__=='__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--feats_folder', help = "Folder with .wav files")
	parser.add_argument('-o', '--output_folder', help = "Output folder for h5f files")
      parser.add_argument('-n', '--name', default='posteriors', help = "Folder with .wav files")
	args = parser.parse_args()
	print("Start generating Features")
	print("Input folder : " + args.feats_folder)
	print("Output folder : " + args.output_folder)	
	make_features(args.feats_folder, args.output_folder, args.name)
	


