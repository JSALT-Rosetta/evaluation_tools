#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:41:30 2017

@author: elinlarsen
"""
import os
import pandas as pd
import argparse

def phoneme_to_speaker_item_file(item_file, unit_colname="#phoneme", spk_colname="speakerID"): 
    
    direc=os.path.dirname(item_file)
    df=pd.read_table(item_file, sep="\t", header=0)
    df.rename(columns={spk_colname: "#speakerID", unit_colname: "phoneme"}, inplace=True)
    print(df.columns)
    c=df.columns.tolist()
    i=c.index("#speakerID")
    j=c.index("phoneme")
    c[i], c[j]=c[j], c[i]

    df=df[c]    
    df.to_csv(direc+ "/speaker.item", sep="\t", header=True, index=False)
    
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--item_file', type=str, help="path to the phoneme file to be transformed to a speaker item file")
    parser.add_argument('-u', '--unit_colname', type=str, default="#phoneme", help="name of the unit column to take out the #")
    parser.add_argument('-s', '--spk_colname', type=str, default="speakerID", help="name of the speaker column to add a #")

    args=parser.parse_args()
    phoneme_to_speaker_item_file(args.item_file, args.unit_colname, args.spk_colname)    
    
