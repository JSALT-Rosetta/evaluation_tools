#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:41:30 2017

@author: elinlarsen
"""
import os
import pandas as pd
import argparse

def phoneme_to_speaker_item_file(item_file): 
    
    direc=os.path.dirname(item_file)
    df=pd.read_table(item_file, sep="\t", header=0)
    df.rename(columns={'speaker_id': '#speakerID',}, inplace=True)
    df.rename(columns={'#phoneme': 'phoneme',}, inplace=True)
    
    c=df.columns
    i=c.index("#speakerID")
    j=c.index("phoneme")
    c[i], c[j]=c[j], c[i]

    df=df[c]    
    df.to_csv(direc+ "speaker.item", sep="\t", header=True, index=False)
    
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--i', type=str, help="path to the phoneme file to be transformed to a speaker item file")

    args=parser.parse_args()
    phoneme_to_speaker_item_file(args.item_file)    
    
