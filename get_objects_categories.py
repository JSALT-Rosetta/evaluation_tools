#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 17:38:36 2017

@author: elinlarsen
"""
import os 
from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import json

# Throughout the API "ann"=annotation, "cat"=category, and "img"=image.

#path_annotations="/pylon2/ci560op/larsene/data/mscoco/annotations/instances_train2014.json"
#coco_train=COCO(path_annotations)
#categories= coco_train.loadCats(coco_train.getCatIds())



def build_dict_cat_name_to_cat_id(categories):
    dict_id_name={}
    for dd in categories :
        dict_id_name[dd['id']]=dd['name']
    return(dict_id_name)
    
def build_dict_cat_name_to_img_id(categories, coco ,save=False, name=""):
    d={}
    for cat in categories: 
        imgIds=coco.getImgIds(catIds=cat['id'])
        d[cat['name']]=imgIds
    if save: 
        with open(name, 'w') as fp:
            json.dump(d, fp)
    return(d)

def reverse_dic(dic, save=False, name=""):
    d = {}
    for key, values in dic.items():
        for value in values:
            d.setdefault(value, []).append(key)
    if save: 
        with open(name, 'w') as fp:
            json.dump(d, fp)
    return(d)

def dict_nb_value_per_key(dic):    
    d={}
    for key, value in dic.items():
        d[key]=len(value)
    plt.bar(list(d.keys()), d.values(), color='g')
    plt.show()
    return(d)

'''
#tests
d_cat_to_img=build_dict_cat_name_to_img_id(categories, coco_train)
with open('dict_cat_name_to_img_id.json', 'w') as fp:
    json.dump(d_img_to_cat, fp)
    
    
with open('dict_img_id_to_cat_name.json', 'w') as fp:
    json.dump(d, fp)
    
with open('dict_cat_name_to_img_id.json', 'w') as fp:
    json.dump(d_img_to_cat, fp)    

with open('dict_cat_id_to_name.json', 'w') as fp:
    json.dump(dic_id_name, fp)    
''' 
    
