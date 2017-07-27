#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 18:17:28 2017

@author: elinlarsen
"""
import pandas as pd
import argparse


def select_rows(item_file, wave_file_names, output):

    
    df=pd.read_csv(item_file, sep='\t', header=0)
    try : 
        df.drop("Unnamed: 0", axis=1, inplace=True)
    except: 
        pass
    
    lines = [line.split('.')[0] for line in open(wave_file_names, 'r')]
    
    selected=df[df.iloc[:,0].isin(lines)]
    
    selected.to_csv(output, sep='\t', header=True, index=False)
    return(selected)


if __name__=="__main__":
     
     parser = argparse.ArgumentParser(description='Select audio file names in the item file')
     
     parser.add_argument('-i', '--item_file', help='absolute path of the item file for the ABX task')
     parser.add_argument('-w', '--wave_file_names', help='absolute path of the file containing a list of audio file names')
     parser.add_argument('-o', '--output', help='name of the output item file')
     args=parser.parse_args()
     
     select_rows(item_file=args.item_file, wave_file_names=args.wave_file_names, output=args.output)

