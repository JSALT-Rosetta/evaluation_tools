#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 17:19:26 2017

@author: elinlarsen
"""

import argparse
import speechcoco.speechcoco as sp


## create the whole phoneme item file 
def write_row(output_file, column, jump=True): 
    if jump:
        output_file.write('\n')
    
    output_file.write('\t{}'.format(column))
    '''for el in columns:
        el_str = str(el)
        output_file.write('\t{}'.format(el_str))
    '''
    

def write_phoneme_item_file(db, path_output, name_item_file, columns_names_list, alignment=False):
    """
    Write an item file for an ABX task on phonemes.
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
         "#filename", "onset", "offset", "#phoneme"
         if alignment=False, then columns such as "context", "image ID", 
         "captionID", "speaker IF", "speaker nationality",  can be added
    alignment : boolean, 
         if True , onset and offset of phonemes
         else onset and offset of triphones
    """
    
    captions=db.filterCaptions() # captions and metadata from the SQL database
    
    with open(path_output+"/" + name_item_file,'w' ) as f: 
        try : 
            for ii in range(len(columns_names_list)): 
                write_row(f, columns_names_list[ii], False)
            
            for caption in captions : 
                phonemes = [phoneme for words in caption.timecode.parse() 
                            for syllables in words["syllable"] for phoneme in
                            syllables["phoneme"]]
                
                # for each phoneme create a row with different columns
                for i in range(len(phonemes)): 
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
                            write_row(f,caption.captionID, False)
                            write_row(f,caption.speaker.name, False)
                            write_row(f,caption.speaker.nationality, False)
                
        finally: f.close()
                
                               
def write_word_item_file(db, path_output, name_item_file, columns_names_list, alignment=False):
    """
    Write an item file for an ABX task on words.
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
         "#filename", "onset", "offset", "#word"
         if alignment=False, then columns such as  "image ID", 
         "captionID", "speaker IF", "speaker nationality",  can be added
    alignment : boolean
    """
    captions=db.filterCaptions() # captions and metadata from the SQL database
    
    with open(path_output+ "/" + name_item_file,'w' ) as f: 
        try : 
            for ii in range(len(columns_names_list)): 
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
                            write_row(f,caption.captionID, False)
                            write_row(f,caption.speaker.name, False)
                            write_row(f,caption.speaker.nationality, False)
                
        finally: f.close()
                



parser = argparse.ArgumentParser(description='Write an item or alignment file for an ABX task')

parser.add_argument(
    '-s', '--source', type=str, metavar='<str>',
    help='path of the source language SQL database containing written captions of images')

parser.add_argument(
    '-t', '--target', type=str, metavar='<int>', 
    help='path of the target language SQL database containing written captions of images')

parser.add_argument(
    '-o', '--output', type=str, help='path to output the file')

parser.add_argument(
     '--on', type=str, default="phoneme",
     help='''item on which the abx task will be (phoneme, word or object category),
    default is %(default)s.''')

parser.add_argument(
     '-n', '--columns_names', type=list, default=["#file_name", "onset", "offset", "#phoneme", 
     "context", "imageID", "captionID", "speakerID", "speaker_nationality"],
     help='''list of the columns names of the item file, default is %(default)s.''')

parser.add_argument(
     '-a', '--alignment', type=bool, default=False,
     help='''By default, the alignment is on triphone''')





if __name__=='__main__':
    """Entry point of the 'item_data_mscoco' command"""
    
    args=parser.parse_args()

    db = sp.SpeechCoco(args.source,args.target,verbose=True)  ## SQL database
    
    if args.on=="phoneme":
        write_phoneme_item_file(db, args.output, args.on+".item", args.columns_names, args.alignment)
    
    elif args.on=="word": 
        write_word_item_file(db, args.output, str(args.on)+".item", args.columns_names, args.alignment)
  
    
    
    
    


    



