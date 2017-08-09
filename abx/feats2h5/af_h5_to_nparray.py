#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Aug 9 2017

@author: danny merkx

JSALT 2017
"""

import tables 
import numpy

outpath = '/pylon5/ci560op/dmerkx/af_feats/'
input_path='/pylon2/ci560op/odette/data/flickr/flickr_afs_markus/flickr8_af.h5'

def af_h5_to_np(input_path, outpath):
    
    files = tables.open_file(input_path, mode = 'r+')
    speaker_nodes = files.root._f_list_nodes()
    
    for spk in speaker_nodes:
        file_nodes = spk._f_list_nodes()
        for fls in file_nodes:
            file_name = fls._v_name
            af_nodes = fls._f_list_nodes()
            af_list = []
            for fts in af_nodes:
                features = fts[:]
                mean = numpy.mean(features,1)
                normalised_feats = list(numpy.transpose(features)/mean)
                af_list += normalised_feats
            numpy.save(outpath + file_name, numpy.array(af_list))
