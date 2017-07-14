#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 17:36:03 2017

@author: elinlarsen
"""

from pycocotools.coco import COCO
import get_objects_categories
import MH_sampling
import numpy as np
from collections import defaultdict
from os import listdir
from os.path import isfile, join


def run_sample(dataset_type="train", sample_size=6000, 
               path_ann="/pylon2/ci560op/larsene/data/mscoco/train2014/instances_train2014.json", 
               input_path="/pylon2/ci560op/odette/data/mscoco/train2014/", output="/pylon2/ci560op/larsene/data/8K_mscoco/", 
               speakers=["Phil","Paul", "Amanda", "Judith", "Bruce", "Elizabeth" ], n=4):
    
    coco=COCO(path_ann)
    categories= coco.loadCats(coco.getCatIds())
    d_cat_to_img=get_objects_categories.build_dict_cat_name_to_img_id(categories, coco ,save=False, name="", type_category="supercategory")
    d_img_to_cat=get_objects_categories.reverse_dic(d_cat_to_img, save=False, name="")
    
    print("selecting wave file names according to speaker names...")
    wave_file_name_selected=MH_sampling.select_speaker_in_wav(input_path  + "/wav/", speakers)
    np.array(wave_file_name_selected).dump(open(output+"/" + dataset_type+"/wav/"+'wave_file_name_spk_selected.npy', 'wb'))

    print("selecting image that have 4 captions ...")
    ImgID_selected=list(MH_sampling.get_nb_caption_per_img(n, wave_file_name_selected))
    np.array(ImgID_selected).dump(open(output+"/" + dataset_type+ "/jpg/" +'ImgID_4_captions.npy', 'wb'))
    
    print("sampling selected images ...")
    final_img_selected=MH_sampling.sample_img_id(d_img_to_cat, ImgID_selected, output, int(sample_size),False, replace=False)
    np.array(final_img_selected).dump(open(output+ dataset_type+ "/jpg/"+'ImgID_sample.npy', 'wb'))

    print("create text file with sample of audio file name")
    wav_file_name_sample=MH_sampling.get_wav_file_name_from_ImgID(ImgID_selected, input_path  + "/wav/", output+ dataset_type+"/wav/")
    
    print("create text file with sample of image file name")
    img_file_name_sample=MH_sampling.get_Img_file_name_from_ID(final_img_selected, pre_name="COCO_", train=True, output_path=output+ dataset_type +"/jpg/")
    
    print("image and audio image files written")

