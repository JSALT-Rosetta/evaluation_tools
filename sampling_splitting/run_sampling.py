#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 17:36:03 2017

@author: elinlarsen
"""

import sampling
import dictionnaries
from pycocotools.coco import COCO

def run_sample(dataset_type="test", 
               sample_size=1000, 
               path_ann="/pylon2/ci560op/larsene/data/mscoco/val2014/instances_val2014.json", 
               input_path="/pylon2/ci560op/odette/data/mscoco/val2014/", 
               output="/pylon2/ci560op/larsene/data/8K_mscoco/", 
               dic_speakers={"Phil": 0.5 ,
                                     "Paul": 0.5,
                                     "Amanda":0.5,
                                     "Judith":0.5, 
                                     "Bruce":0.5, 
                                     "Elizabeth":0.5 
                                     }, 
               n=1): 
    
    coco=COCO(path_ann)
    categories= coco.loadCats(coco.getCatIds())
    d_cat_to_img=dictionnaries.build_dict_cat_name_to_img_id(categories, coco ,save=False, name="", type_category="supercategory")
    d_img_to_cat=dictionnaries.reverse_dic(d_cat_to_img, save=False, name="")
    
    print("selecting wave file names according to speaker names...")
    wave_file_name_selected=sampling.select_speaker_in_wav(input_path  + "/wav/", dic_speakers)
     
    print("selecting image that have 4 captions ...")
    ImgID_selected=list(sampling.get_nb_caption_per_img(n, wave_file_name_selected))
    
    print("sampling selected images ...")
    final_img_selected=sampling.sample_img_id(d_img_to_cat, ImgID_selected, output, int(sample_size),False, replace=False)
    
    print("create text file with sample of audio file name")
    wav_file_name_sample=sampling.get_wav_file_name_from_ImgID(final_img_selected, wave_file_name_selected, output+ dataset_type+"/wav/")
    
    print("create text file with sample of image file name")
    img_file_name_sample=sampling.get_Img_file_name_from_ID(final_img_selected, pre_name="COCO_", train=True, output_path=output+ dataset_type +"/jpg/")
    
    print("image and audio image files written")


