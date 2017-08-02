# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:02:38 2017

@author: elinlarsen
"""

'''
Script generating an item file for the ABX tsk done on the Mboshi dataset 

'''

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import argparse
import pdb

import generate_item_file_flickr

    

def get_item_file(path_alignment, output_dir, on='phoneme', phone_alignment=False):
    alignnames=[f for f in listdir(path_alignment) if isfile(join(path_alignment, f))]
    speakerID=[f.split('_')[0] for f in alignnames]
    wavnames=['_'.join(f.split('_')[1:]) for f in alignnames]
    
    df_names=pd.DataFrame({'align': alignnames,
                            'speakerID': speakerID,
                            '#file': wavnames
                            })
   
    df_item=pd.DataFrame()
    for ii  in range(len(df_names)):
          
        if on=='phoneme':
            d_align=pd.read_table(path_alignment+ df_names['align'][ii], header=None, sep=" ", names=['#phoneme', 'onset', 'offset'])
                       
        elif on=='word':
            d_align=pd.read_table(path_alignment+df_names['align'][ii], header=None, sep=" ", names=['#word', 'onset', 'offset'])
        
        cols = d_align.columns.tolist()
        cols = cols[1:]+cols[0:1]
        d_align = d_align[cols] 

        filename=df_names['#file'][ii].split('.')[0]        
        df_filename=pd.DataFrame(np.repeat(filename , len(d_align)), columns=['#file'])
        df_speakerID=pd.DataFrame(np.repeat(df_names['speakerID'][ii], len(d_align)), columns=['speakerID'])
        d=pd.concat([df_filename, d_align, df_speakerID], axis=1) 
        
        if phone_alignment==False:
            triphone_align=generate_item_file_flickr.phone_to_triphone_alignment(d)
            context=generate_item_file_flickr.create_phonetic_context(triphone_align, on)
        else:
            #context=generate_item_file_flickr.create_phonetic_context(d, on)
            pdb.set_state()
        
        df_item=pd.concat([df_item, context], axis=0)  
                
    print('removing side info and saving into text file')
    if on=='phoneme':
        item = df_item[df_item["#phoneme"] != "+LAUGH+"]
        item = item[item["#phoneme"] != "SIL"]
        item = item[item["#phoneme"] != "+NOISE+"]
        item = item[item["#phoneme"] != "+BREATH+"]
        item = item[item["#phoneme"] != "+HUMAN+"]
        item.to_csv( output_dir+ "phoneme.item", sep='\t', header=True, index=False )
    elif on=='word':
        item = df_item[df_item["#word"] != "+LAUGH+"]
        item = item[item["#word"] != "SIL"]
        item = item[item["#word"] != "+NOISE+"]
        item = item[item["#word"] != "+BREATH+"]
        item = item[item["#word"] != "+HUMAN+"]
        item.to_csv( output_dir+ "word.item", sep='\t', header=True, index=False)
        
    return(item)


    
parser = argparse.ArgumentParser(description='Write an item or a phone alignment file for an ABX task')

parser.add_argument(
    '-p', '--path_alignment', type=str, metavar='<str>',
    help='path of the directory containing all the alignement files for each audio caption')

parser.add_argument(
    '-o', '--output_dir', type=str, help='''path of text file containing 
    dataframe with wave filenames, dataset type and speaker ID as columns''')

parser.add_argument(
     '--on', type=str, default="phoneme",
     help='''item on which the abx task will be (phoneme, word or speakerID),
    default is %(default)s.''')

parser.add_argument(
     '-a', '--phone_alignment', type=bool, default=False,
     help='''By default, the alignment is on triphone''')




if __name__=='__main__':
    """Entry point of the 'item_data_mscoco' command"""
    
    args=parser.parse_args()    
   
    get_item_file(args.path_alignment, args.output_dir , args.on, args.phone_alignment)
    

######### TERMINAL command

#path_align ="/pylon2/ci560op/odette/data/mboshi-french-parallel-corpus/forced_alignments_supervised_spkr/train/"
#path_wav="/pylon2/ci560op/odette/data/mboshi-french-parallel-corpus/full_corpus/train/"
#path_mfcc="/pylon2/ci560op/odette/data/mboshi-french-parallel-corpus/incoming/xnmt_train/mfcc.h5f"

#python generate_item_file_mboshi.py -p "/pylon2/ci560op/odette/data/mboshi-french-parallel-corpus/forced_alignments_supervised_spkr/" -o '/pylon5/ci560op/larsene/abx/mboshi/train/mfcc/' --on 'phoneme' 
##########   
    
