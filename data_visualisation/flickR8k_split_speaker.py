#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 17:25:54 2017

@author: elinlarsen
"""

import os 
import pandas as pd 
import numpy as np
import pylab as pl
from pandas import *
os.getcwd()

os.chdir("/Users/elinlarsen/Documents/2017_JSALT/flickR8K/")
#image id name
train=pd.read_csv("/Users/elinlarsen/Documents/2017_JSALT/flickR8K/train/Flickr_8k.trainImages.txt", names = ["wave_file"])
dev=pd.read_csv("/Users/elinlarsen/Documents/2017_JSALT/flickR8K/dev/Flickr_8k.devImages.txt", names = ["wave_file"])
test=pd.read_csv("/Users/elinlarsen/Documents/2017_JSALT/flickR8K/test/Flickr_8k.testImages.txt", names = ["wave_file"])

#add caption number
def add_caption_number(df, column_name):
    l=[]
    for ii in df[column_name]:
        s=ii.split(".")[0]
        for nb in range(0,5):
            l.append(s+"_"+ str(nb)+".wav")
    new_df=pd.DataFrame({column_name:l})
    return(new_df)


train=add_caption_number(train, "wave_file")
train["dataset"]=np.repeat("train",len(train))

dev=add_caption_number(dev, "wave_file")
dev["dataset"]=np.repeat("dev",len(dev))

test=add_caption_number(test, "wave_file")
test["dataset"]=np.repeat("test",len(test))

flickR8k=pd.concat([train, dev])
flickR8k=pd.concat([flickR8k, test])



wav2spk=pd.read_csv("/Users/elinlarsen/Documents/2017_JSALT/flickR8K/wav2spk.txt", delimiter=r"\s+", names = ["wave_file", "speaker_id"])
flickR8k=pd.merge(flickR8k, wav2spk, on="wave_file", how="inner")
flickR8k.to_csv("/Users/elinlarsen/Documents/2017_JSALT/flickR8K/df_wav_spk_set.txt", header=True, index=False, sep="\t")
flickR8k.to_csv("/pylon2/ci560op/odette/data/flickr/df_wav_spk_set.txt")

gp_train=flickR8k.groupby("dataset").get_group("train")
gp_dev=flickR8k.groupby("dataset").get_group("dev")
gp_test=flickR8k.groupby("dataset").get_group("test")



gp_spk_train=gp_train.groupby("speaker_id")
gp_spk_dev=gp_dev.groupby("speaker_id")
gp_spk_test=gp_test.groupby("speaker_id")

spk_train=gp_spk_train.groups.keys()
spk_dev=gp_spk_dev.groups.keys()
spk_test=gp_spk_test.groups.keys()



gp_train.hist(figsize=(9,12))
pl.suptitle("Number of captions read by 183 speakers in the training set")
pl.savefig('Nb_Caption_Per_Spk_train.jpg')

gp_dev.hist(figsize=(9,12))
pl.suptitle("Number of captions read by 183 speakers in the development set")
pl.savefig('Nb_Caption_Per_Spk_dev.jpg')

gp_test.hist(figsize=(9,12))
pl.suptitle("Number of captions read by 183 speakers in the testing set")
pl.savefig('Nb_Caption_Per_Spk_test.jpg')

