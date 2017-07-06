#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 17:19:26 2017

@author: elinlarsen
"""

import os
import csv
import speechcoco.speechcoco as sp

path_val_sql="../val2014/val_2014.sqlite3" # SQL database on validation dataset ( ~ 200 k  English captions)
path_tra_sql="../val2014/tra/val_translate.sqlite3" # SQL translation (Japanese) database on validation dataset ( ~ 200 k captions)
path_output='/pylon2/ci560op/larsene/abx_eval/mscoco/'

db = sp.SpeechCoco(path_val_sql,path_tra_sql,verbose=True) # SQL database


## create the whole phoneme item file 
def write_row(output_file, columns, jump=True): 
    if jump:
        output_file.write('\n')
    
    for el in columns:
        el_str = str(el)
        output_file.write('\t{}'.format(el_str))
    

def write_phoneme_item_file(db, path_output, name_item_file, columns_names_list, alignment=False):
    """Write an item file for an ABX task on phonemes.
    Parameters
    ----------
    db : SQLite3 database containing meta-data about SpeechCoco  
         dataset created from the SpeechCoco database
    path_output : string,
         absolute path where to put the item file
    name_item_file : string,    
         name of the item file
    columns_names_list: list,
         list of the columns of the item file, must be at least in that order
         "name of the image_caption file", "onset", "offset", "phoneme"
         if alignment=False, then columns such as "context", "image ID", 
         "captionID", "speaker IF", "speaker nationality",  can be added
    alignment : boolean, 
         if True , onset and offset of phonemes
         else onset and offset of triphones
    """
    
    captions=db.filterCaptions() # captions and metadata from the SQL database
    
    with open(path_output+name_item_file,'w' ) as f: 
        try : 
            for ii in len(columns_names_list): 
                write_row(f, columns_names_list[ii], False)
            
            for caption in captions : 
                phonemes = [phoneme for words in caption.timecode.parse() for syllables in words["syllable"] for phoneme in
                            syllables["phoneme"]]
                
                for i in range(len(phonemes)): # for each phoneme create a row with different columns
                    if i!=0 and i!=len(phonemes)-1:
                
                        source=caption.filename.split(".")[0]
                        phoneme=str(phonemes[i]['value'])
                        
                        if alignment: 
                            onset=str(phonemes[i]['begin'])
                            offset=str(phonemes[i]['end'])
                        else :    
                            onset=str(phonemes[i-1]['begin'])
                            offset=str(phonemes[i+1]['end'])
                            context=str('_'.join((phonemes[i-1]['value'], phonemes[i+1]['value'])))
                        
                        write_row(f,source, True)
                        write_row(f,onset, False)
                        write_row(f,offset, False)
                        write_row(f,phoneme, False)
                        
                        if alignment==False : 
                            write_row(f,context, False)
                            write_row(f,caption.imageID, False)
                            write_row(f,caption.speaker.name, False)
                            write_row(f,caption.speaker.nationality, False)
                
        finally: f.close()
                
                               
def write_word_item_file(db, path_output, name_item_file, columns_names_list, alignment=False):
     """Write an item file for an ABX task on words.
    Parameters
    ----------
    db : SQLite3 database containing meta-data about SpeechCoco  
         dataset created from the SpeechCoco database
    path_output : string,
         absolute path where to put the item file
    name_item_file : string,    
         name of the item file
    columns_names_list: list,
         list of the columns of the item file, must be at least in that order
         "name of the image_caption file", "onset", "offset", "word"
         if alignment=False, then columns such as  "image ID", 
         "captionID", "speaker IF", "speaker nationality",  can be added
    alignment : boolean, 
    """
    
    captions=db.filterCaptions() # captions and metadata from the SQL database
    
    with open(path_output+name_item_file,'w' ) as f: 
        try : 
            for ii in len(columns_names_list): 
                write_row(f, columns_names_list[ii], False)
            
            for caption in captions : 
                
                for word in caption.timecode.parse():
                
                        source=caption.filename.split(".")[0]
                        onset=str(word['begin'])
                        offset=str(word['end'])
                        word=str(word['value'])
                        
                        write_row(f,source, True)
                        write_row(f,onset, False)
                        write_row(f,offset, False)
                        write_row(f,word, False)
                        
                        if alignment==False: 
                            write_row(f,caption.imageID, False)
                            write_row(f,caption.speaker.name, False)
                            write_row(f,caption.speaker.nationality, False)
                
        finally: f.close()
                
        

       
    
       
    
'''OLD
with open(path_output+"phoneme_item_file_val2014.txt", 'w') as f:  
    try:
        f.write('\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format('#filename', 'onset', 'offset','#phoneme', 'context', 'imageID','captionID', 'speaker_name','nationality')) 
        for caption in captions : 
            phonemes = [phoneme for words in caption.timecode.parse() for syllables in words["syllable"] for phoneme in
                            syllables["phoneme"]]
            nbTier = len(phonemes)
            for i in range(nbTier):
                if i!=0 and i!=nbTier-1:
                    #list_colonnes
                    #ecrire(f,list_colonnes)
                    f.write('\n{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(caption.filename.split(".")[0],
                                                                  str(phonemes[i-1]['begin']),
                                                                  str(phonemes[i+1]['end']), 
                                                                  str(phonemes[i]['value']), 
                                                                  str('_'.join((phonemes[i-1]['value'], phonemes[i+1]['value']))),
                                                                  caption.imageID,
                                                                  caption.captionID,
                                                                  caption.speaker.name,
                                                                  caption.speaker.nationality,
                                                                  )
    
                            )
    finally: f.close()
 '''   
    

## sample the item file 

