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

from collections import defaultdict

# Throughout the API "ann"=annotation, "cat"=category, and "img"=image.

#path_annotations="/pylon2/ci560op/larsene/data/mscoco/annotations/instances_train2014.json"
#coco_train=COCO(path_annotations)
#categories= coco_train.loadCats(coco_train.getCatIds())
#d_cat_name=get_objects_categories.build_dict_cat_name_to_cat_id(categories)
#d_cat_to_img=get_objects_categories.build_dict_cat_name_to_img_id(categories, coco_train)
#d_img_to_cat=get_objects_categories.reverse_dic(d_cat_to_img, save=False, name="")



def build_dict_cat_name_to_cat_id(categories):
    dict_id_name={}
    for dd in categories :
        dict_id_name[dd['id']]=dd['name']
    return(dict_id_name)
    
def build_dict_cat_name_to_img_id(categories, coco ,save=False, name=""):
    d = defaultdict(set)
    for cat in categories: 
        imgIds=coco.getImgIds(catIds=cat['id'])
        d[cat['name']]=imgIds
    if save: 
        with open(name, 'w') as fp:
            json.dump(d, fp)
    return(d)

def reverse_dic(dic, save=False, name=""):
    """
    For a given dictionary (dic), reverse keys and values. Return a dictionary
    """
    d = defaultdict(set)
    
    for k in dic.keys(): 
        for v in dic.values():
            for ii in v: 
                d[ii].add(k)
        
    if save: 
        with open(name, 'w') as fp:
            json.dump(d, fp)
    return(d)

def dict_nb_value_per_key(dic, show_plot=False):   
    """
    For a given dictionary (dic), compute for each key, the number of values
    Return a dictionary
    """
    d={}
    for key, value in dic.items():
        d[key]=len(value)
    if show_plot:
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
    
