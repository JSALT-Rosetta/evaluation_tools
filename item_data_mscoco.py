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

db = sp.SpeechCoco(path_val_sql,path_tra_sql,verbose=True)


## copy in a text file all the text captions information

captions=db.filterCaptions() # download 

with open(path_output+"caption.txt", 'w') as f : 
    try :
        f.write('\t{}\t{}\t{}\t{}\t{}\t\t{}'.format('imageID','captionID', 'speaker_name', 'nationality', 'speed', 'filename', 'text' )) 
        for caption in captions: 
            f.write( '\n{}\t{}\t{}\t{}\t{}\t{}\t\t{}'.format(caption.imageID,
                                                          caption.captionID,
                                                          caption.speaker.name,
                                                          caption.speaker.nationality,
                                                          caption.speed,
                                                          caption.filename,
                                                          caption.text)
                            ) 
    finally: f.close()


## copy in a text file all the spoken captions information about phoneme

with open(path_output+"phoneme_spoken_caption_val2014.txt", 'w') as f:  
    try:
        f.write('\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format('imageID','captionID', 'speaker_name','nationality',  'phoneme', 'onset', 'offset', 'context')) 
        for caption in captions : 
            phonemes = [phoneme for words in caption.timecode.parse() for syllables in words["syllable"] for phoneme in
                            syllables["phoneme"]]
            nbTier = len(phonemes)
            for i in range(nbTier):
                if i!=0 and i!=nbTier-1:
                    f.write('\n{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(caption.imageID,
                                                                  caption.captionID,
                                                                  caption.speaker.name,
                                                                  caption.speaker.nationality,
                                                                  str(phonemes[i]['value']), 
                                                                  str(phonemes[i-1]['begin']),
                                                                  str(phonemes[i+1]['end']), 
                                                                  str('_'.join((phonemes[i-1]['value'], phonemes[i+1]['value']))),
                                                                  )
    
                            )
    finally: f.close()
    

## copy in a text file all the spoken captions information about words

with open(path_output+"word_spoken_caption_val2014.txt", 'w') as f:  
    try:
        f.write('\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format('imageID','captionID', 'speaker_name','nationality',  'word', 'onset', 'offset')) 
        for caption in captions :
            for word in caption.timecode.parse():
                f.write('\n{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(caption.imageID,
                                                              caption.captionID,
                                                              caption.speaker.name,
                                                              caption.speaker.nationality,
                                                              str(word['value']), 
                                                              str(word['begin']),
                                                              str(word['end'])
                                                              )
                        )                          
    finally: f.close()

