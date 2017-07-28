#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 17:36:03 2017

@author: elinlarsen
"""

import sampling
import dictionnaries
from pycocotools.coco import COCO

def run_sample(dataset_type="dev", 
               sample_size=1000, 
               path_ann="/pylon2/ci560op/larsene/data/mscoco/annotations/instances_val2014.json", 
               input_path="/pylon2/ci560op/odette/data/mscoco/val2014/", 
               output="/pylon2/ci560op/larsene/data/8K_mscoco/", 
               dic_speakers={"Phil": 1/float(6) ,
                             "Paul": 1/float(6),
                             "Amanda":1/float(6),
                             "Judith":1/float(6), 
                             "Bruce":1/float(6), 
                             "Elizabeth":1/float(6), 
                             },
               n=4): 
    
    coco=COCO(path_ann)
    categories= coco.loadCats(coco.getCatIds())
    d_cat_to_img=dictionnaries.build_dict_cat_name_to_img_id(categories, coco ,save=False, name="", type_category="supercategory")
    d_img_to_cat=dictionnaries.reverse_dic(d_cat_to_img, save=False, name="")
    
    print("extracting wav file names as list")
    wave_files=sampling.create_list_from_files_in_folder(input_path+ "/wav/")
    
    if dataset_type=='dev':
        test_subset=sampling.create_list_from_files_in_folder(output+ "/test/wav/")
        wave_files=list(set(wave_files)-set(test_subset))
    
    print("selecting wave file names according to speaker names...")# for the dev test, must be different than the one in the 8Kmscoco test":    
    wave_file_name_selected=sampling.select_speaker_in_wav(wave_files, dic_speakers, output +dataset_type, dataset_type)
     
    print("selecting image that have 4 captions ...")
    ImgID_selected=list(sampling.get_nb_caption_per_img(n, wave_file_name_selected))
    
    print("sampling selected images ...")
    final_img_selected=sampling.sample_img_id(d_img_to_cat, ImgID_selected, output, int(sample_size),False, replace=False)
    
    print("create text file with sample of audio file name")
    wav_file_name_sample=sampling.get_wav_file_name_from_ImgID(final_img_selected, wave_file_name_selected, output+ dataset_type+"/wav/")
    
    print("create text file with sample of image file name")
    img_file_name_sample=sampling.get_Img_file_name_from_ID(final_img_selected, pre_name="COCO_", train=True, output_path=output+ dataset_type +"/jpg/")
    
    print("image and audio image files written")


