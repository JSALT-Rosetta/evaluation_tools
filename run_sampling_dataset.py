#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 17:36:03 2017

@author: elinlarsen
"""

from pycocotools.coco import COCO
import get_objects_categories
import MH_sampling
import time
import numpy as np
from collections import defaultdict
from os import listdir
from os.path import isfile, join


###### TRAINING ####
path_annotations="/pylon2/ci560op/larsene/data/mscoco/train2014/instances_train2014.json"
coco_train=COCO(path_annotations)
categories= coco_train.loadCats(coco_train.getCatIds())



d_cat_name=get_objects_categories.build_dict_cat_name_to_cat_id(categories)
d_cat_to_img=get_objects_categories.build_dict_cat_name_to_img_id(categories, coco_train ,save=False, name="", type_category="supercategory")
d_img_to_cat=get_objects_categories.reverse_dic(d_cat_to_img, save=False, name="")


nb_img=[]
for k, v in  d_cat_to_img_val.items():
    nb_img.append(len(d_cat_to_img_val[k]))
    print(k +" : "+ str(len(d_cat_to_img_val[k])))
    #print(sum(nb_img))


#### TRAINING ####
input_path="/pylon2/ci560op/odette/data/mscoco/train2014/wav"
train_size=0.75
speakers=["Phil","Paul", "Amanda", "Judith", "Bruce", "Elizabeth" ]
n=4
output_path="/pylon2/ci560op/larsene/data/mscoco_8K_by_spk/train/jpg/"
T_0=100
T_fin=1
tau=2
nb_iter=10

start_time = time.time()
print("selecting wave file names according to speaker names...")
wave_file_name_selected=MH_sampling.select_speaker_in_wav(input_path, speakers)
print("--- %s seconds ---" % (time.time() - start_time))
np.array(wave_file_name_selected).dump(open("/pylon2/ci560op/larsene/data/mscoco_8K_by_spk/train/wav/"+'wave_file_name_spk_selected.npy', 'wb'))

#np.load("/pylon2/ci560op/larsene/data/subset_mscoco/train/old_sample"+'wave_file_name_selected.npy')

start_time = time.time()
print("selecting image that have 4 captions ...")
ImgID_selected=MH_sampling.get_nb_caption_per_img(n, wave_file_name_selected)
ImgID_selected_list=list(ImgID_selected)
print("--- %s seconds ---" % (time.time() - start_time))

np.array(ImgID_selected_list).dump(open("/pylon2/ci560op/larsene/data/mscoco_8K_by_spk/train/jpg"+'ImgID_4_captions.npy', 'wb'))

#np.load("/pylon2/ci560op/larsene/data/subset_mscoco/train/test/"+'ImgID_selected.npy')


start_time = time.time()
print("sampling selected images ...")
final_img_selected=MH_sampling.sample_img_id(d_img_to_cat, ImgID_selected_list, output_path, int(sample_size*train_size),False,  T_0, T_fin, tau, nb_iter,  replace=False)
print("--- %s seconds ---" % (time.time() - start_time))

np.array(final_img_selected).dump(open("/pylon2/ci560op/larsene/data/mscoco_8K_by_spk/train/jpg/"+'ImgID_sample_train.npy', 'wb'))


img_file_name_sample=get_Img_file_name_from_ID(final_img_selected, pre_name="COCO_", train=True, output_path="/pylon2/ci560op/larsene/data/mscoco_8K_by_spk/train/jpg/")

wav_file_path="/pylon2/ci560op/odette/data/mscoco/train2014/wav"
wav_file_name_sample=get_wav_file_name_from_ImgID(final_img_selected, wav_file_path, output_path="/pylon2/ci560op/larsene/data/mscoco_8K_by_spk/train/wav/")
np.save(wav_file_name_sample)


#### DEV ####



#### TEST ####
sample_size=8000
coco_val=COCO("/pylon2/ci560op/larsene/data/mscoco/val2014/instances_val2014.json")
categories_val= coco_val.loadCats(coco_val.getCatIds())
d_cat_to_img_val=get_objects_categories.build_dict_cat_name_to_img_id(categories, coco_val ,save=False, name="", type_category="supercategory")
d_img_to_cat_val=get_objects_categories.reverse_dic(d_cat_to_img_val, save=False, name="")

train_size=0.125
speakers=[ "Bruce", "Elizabeth",  "Jenny", "Bronwen"]
n=4
input_path="/pylon2/ci560op/odette/data/mscoco/val2014/wav"
output_path="/pylon2/ci560op/larsene/data/mscoco_8K_by_spk/test/"

start_time = time.time()
print("selecting wave file names according to speaker names...")
wave_file_name_selected=MH_sampling.select_speaker_in_wav(input_path, speakers)
print("--- %s seconds ---" % (time.time() - start_time))
np.array(wave_file_name_selected).dump(open(output_path+"/wav/"+'wave_file_name_spk_selected.npy', 'wb'))

#np.load(""/pylon2/ci560op/larsene/data/mscoco_8K_by_spk/val/wav/"+'wave_file_name_spk_selected.npy')

start_time = time.time()
print("selecting image that have 4 captions ...")
ImgID_selected=MH_sampling.get_nb_caption_per_img(n, wave_file_name_selected)
ImgID_selected_list=list(ImgID_selected)
print("--- %s seconds ---" % (time.time() - start_time))

np.array(ImgID_selected_list).dump(open(output_path+"/jpg/"+'ImgID_4_captions.npy', 'wb'))

#np.load("/pylon2/ci560op/larsene/data/subset_mscoco/train/test/"+'ImgID_selected.npy')


start_time = time.time()
print("sampling selected images ...")
final_img_selected=MH_sampling.sample_img_id(d_img_to_cat_val, ImgID_selected_list, output_path, int(sample_size*train_size),False,  T_0="", T_fin="", tau="", nb_iter="",  replace=False)
print("--- %s seconds ---" % (time.time() - start_time))

np.array(final_img_selected).dump(open(output_path+"/jpg/"+'ImgID_sample_test.npy', 'wb'))


img_file_name_sample=get_Img_file_name_from_ID(final_img_selected,"COCO_", False, output_path+"/jpg/")

wav_file_path="/pylon2/ci560op/odette/data/mscoco/val2014/wav"
wav_file_name_sample=get_wav_file_name_from_ImgID(final_img_selected, wav_file_path, output_path+"/wav/")

