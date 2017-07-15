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

dic_speakers={"Phil": 0.5 ,
             "Paul": 0.5,
             "Amanda":0.5,
             "Judith":0.5, 
             "Bruce":0.5, 
             "Elizabeth":0.5 
        }
def run_sample(dataset_type="test", sample_size=1000, path_ann="/pylon2/ci560op/larsene/data/mscoco/val2014/instances_val2014.json", input_path="/pylon2/ci560op/odette/data/mscoco/val2014/", output="/pylon2/ci560op/larsene/data/8K_mscoco/", speakers=dic_speakers, n=1): 
    coco=COCO(path_ann)
    categories= coco.loadCats(coco.getCatIds())
    d_cat_to_img=get_objects_categories.build_dict_cat_name_to_img_id(categories, coco ,save=False, name="", type_category="supercategory")
    d_img_to_cat=get_objects_categories.reverse_dic(d_cat_to_img, save=False, name="")
    
    print("selecting wave file names according to speaker names...")
    wave_file_name_selected=MH_sampling.select_speaker_in_wav(input_path  + "/wav/", speakers)
     
    print("selecting image that have 4 captions ...")
    ImgID_selected=list(MH_sampling.get_nb_caption_per_img(n, wave_file_name_selected))
    
    print("sampling selected images ...")
    final_img_selected=MH_sampling.sample_img_id(d_img_to_cat, ImgID_selected, output, int(sample_size),False, replace=False)
    
    print("create text file with sample of audio file name")
    wav_file_name_sample=MH_sampling.get_wav_file_name_from_ImgID(final_img_selected, wave_file_name_selected, output+ dataset_type+"/wav/")
    
    print("create text file with sample of image file name")
    img_file_name_sample=MH_sampling.get_Img_file_name_from_ID(final_img_selected, pre_name="COCO_", train=True, output_path=output+ dataset_type +"/jpg/")
    
    print("image and audio image files written")


#TRAINING and DEV 
dic_speakers={"Phil": 0.5 ,
             "Paul": 0.5,
             "Amanda":0.5,
             "Judith":0.5, 
             "Bruce":0.5, 
             "Elizabeth":0.5 
        }
dataset="train"
size=7000
path_ann="/pylon2/ci560op/larsene/data/mscoco/train2014/instances_train2014.json"
output="/pylon2/ci560op/odette/data/8K_mscoco/"
input_path="/pylon2/ci560op/odette/data/mscoco/train2014/"
n=4
run_sample(dataset, size,path_ann,  input_path, output, speakers=dic_speakers)

# THEN DIVIDE 6000 images for the train and 1000 for the dev


#test
dic_speakers={"Phil": 1/float(12) ,
             "Paul": 1/float(12),
             "Amanda":1/float(12),
             "Judith":1/float(12), 
             "Bruce":1/float(12), 
             "Elizabeth":1/float(12), 
             "Bronwen":0.25, 
             "Jenny":0.25 , 
        }
dataset="test"
size=1000
path_ann="/pylon2/ci560op/larsene/data/mscoco/val2014/instances_val2014.json"
output="/pylon2/ci560op/odette/data/8K_mscoco/"
input_path="/pylon2/ci560op/odette/data/mscoco/val2014/"
n=1
run_sample(dataset, size,path_ann,  input_path, output, speakers=dic_speakers)
