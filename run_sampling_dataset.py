#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 17:36:03 2017

@author: elinlarsen
"""

from pycocotools.coco import COCO
import get_objects_categories
import MH_sampling

path_annotations="/pylon2/ci560op/larsene/data/mscoco/train2014/instances_train2014.json"
coco_train=COCO(path_annotations)
categories= coco_train.loadCats(coco_train.getCatIds())
d_cat_name=get_objects_categories.build_dict_cat_name_to_cat_id(categories)
d_cat_to_img=get_objects_categories.build_dict_cat_name_to_img_id(categories, coco_train)
d_img_to_cat=get_objects_categories.reverse_dic(d_cat_to_img, save=False, name="")

sample_size=8000


#### TRAINING ####
input_path="/pylon2/ci560op/odette/data/mscoco/train2014/wav"
train_size=0.8
speakers=["Phil","Paul", "Amanda", "Judith", "Bruce", "Elizabeth" ]
n=4
output_path="/pylon2/ci560op/larsene/data/subset_mscoco/train/jpg"
T_0=100
T_fin=1
tau=2
nb_iter=10

print("selecting wave file names according to speaker names...")
wave_file_name_selected=MH_sampling.select_speaker_in_wav(input_path, speakers)

print("selecting image that have 4 captions ...")
ImgID_selected=MH_sampling.get_nb_caption_per_img(n, wave_file_name_selected)
ImgID_selected_list=list(ImgID_selected)


print("sampling selected images ...")
final_img_selected=MH_sampling.sample_img_id(d_img_to_cat, ImgID_selected_list, output_path, int(sample_size*train_size), T_0, T_fin, tau, nb_iter,  replace=False)
