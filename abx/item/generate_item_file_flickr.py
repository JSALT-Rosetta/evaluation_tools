# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:30:12 2017

@author: doctor
"""

"""
Generating an item file for the ABX task on Flickr 8K
"""

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import argparse



def create_list_from_files_in_folder(input_path): 
    files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    return(files)


def get_wavname_from_alignment(path_alignement):
    
    align_filename= create_list_from_files_in_folder(path_alignement)
    wavname=[('_'.join(f.split("_")[1:])).split(".")[0] for f in align_filename]
    return(wavname)


def phone_to_triphone_alignment(df):
    """
    df dataframe must have as columns onset and offset of phonemes
    The function returns a dataframe with colunms of onset and offset of triphones
    """
    triphones_onset=[]
    triphones_offset=[]
    
    new_df=df.copy(deep=True)
    filenames=reduce(lambda l, x: l if x in l else l+[x], df["#file"], []) # get all filenames in ORDER (do not use set())
    for f in filenames: 
        sub=df[df["#file"]==f]   #subset the dataframe for one filename (caption)                         
        for i in range(len(sub)):
            if i==0:
                triphones_onset.append(sub.iloc[i]["onset"])
            else:
                triphones_onset.append(sub.iloc[i-1]["onset"]) 
                   
            if i==len(sub)-1:
                triphones_offset.append(sub.iloc[i]["offset"])
            else:
                triphones_offset.append(sub.iloc[i+1]["offset"])
             
    new_df['onset']=triphones_onset
    new_df['offset']=triphones_offset
    return(new_df)      


def dic_alignment_to_wave(path_alignement):  
    dic={}
    align_filename= create_list_from_files_in_folder(path_alignement)
    wavname=[('_'.join(f.split("_")[1:])).split(".")[0] for f in align_filename]
    for i in range(len(align_filename)):
        dic[align_filename[i]]= wavname[i] 
    return(dic)

def create_phonetic_context(df, on='phoneme'):
    """
    From a dataframe containing a colunms of phones, create another column 
    containing previous and following phones for each phone
    """
    list_context=[]
      
    filenames=reduce(lambda l, x: l if x in l else l+[x], df["#file"], []) # get all filenames in ORDER (do not use set())
    for f in filenames: 
        sub=df[df["#file"]==f]   #subset the dataframe for one filename (caption)     
        if on=='phoneme':
            phonemes=list(sub["#phoneme"])
        else:
            phonemes=list(sub['phoneme'])                    
        L=len(sub)
        for i in range(L):
            if i!=0 and i!=L-1:
                context="_".join((phonemes[i-1], phonemes[i+1]))
                list_context.append(context)
            elif i==0:
                context="_".join(("BEGIN", phonemes[i+1]))
                list_context.append(context)
            elif i==L-1:
                context="_".join((phonemes[i-1], "END"))
                list_context.append(context)          
    df["context"]=list_context
    return(df)
    
path_alignment="/pylon5/ci560op/larsene/abx/flickr/flickr_labels"
dataset_type="test"
path_wav_spk_datasetype='/pylon5/ci560op/larsene/abx/flickr/df_wav_spk_set.txt'
output_dir='/pylon5/ci560op/larsene/abx/flickr/test/mfcc/'
on='phoneme'

    
def get_item_file(path_alignment, dataset_type, path_wav_spk_datasetype, output_dir , on="phoneme", phone_alignment=False):
    '''
    Create a text file containing a dataframe corresponding to an item file for the ABX task
    '''    
     
    #### transformation of the dataset containing speaker ID, dataset type for each wave file ####
    print('opening wave to speaker and dataset file')
    df=pd.read_table(path_wav_spk_datasetype, sep='\t', header=0)  
    if on=='speakerID':
        df.rename(columns={'speaker_id': '#speakerID', 'wave_file':'#file'}, inplace=True)
    else:
        df.rename(columns={'speaker_id': 'speakerID', 'wave_file':'#file'}, inplace=True)     
    df["#file"]=[f.split(".")[0] for f in df["#file"]] # get rid of extension in file name
    df_set=df[df['dataset']==dataset_type] # subset the dataset to the set (train, dev or test)
    
    #### read all alignment files and get a dataframe with context and speaker ID info ####
    print('opining all alignment files')
    dic=dic_alignment_to_wave(path_alignment)
    dic_rev=dict((v, k) for k, v in dic.iteritems()) 
    selected_align=[]  
    alignfiles= [v for k,v in dic.items()]
    wav_set=set(alignfiles).intersection(set(df_set['#file']))
    for w in wav_set:
        selected_align.append(dic_rev[w])
    df_align=pd.DataFrame()
    print('colunms transformation for each alignment file and concatenation into a dataframe')
    for filename in selected_align:
        if on=='phoneme':
            d=pd.read_table(path_alignment+filename, header=None, sep=" ", names=['#phoneme', 'onset', 'offset'])
        elif on=='speakerID' :
            d=pd.read_table(path_alignment+filename, header=None, sep=" ", names=['phoneme', 'onset', 'offset'])
        elif on=='word':
            d=pd.read_table(path_alignment+filename, header=None, sep=" ", names=['#word', 'onset', 'offset'])
        cols = d.columns.tolist()
        cols = cols[1:]+cols[0:1]
        d = d[cols] 
        df_filename=pd.DataFrame(np.repeat(dic[filename], len(d)), columns=['#file'])
        if phone_alignment==False:
            triphone_align=phone_to_triphone_alignment(d)
            context=create_phonetic_context(triphone_align, on)
        else:
            context=create_phonetic_context(d, on)
        dd=pd.concat([df_filename, context], axis=1)
        df_align=pd.concat([df_align, dd], axis=0)    
    final=pd.merge(df_align, df_set, on='#file', how="inner")
    
    #### remove all non phonetic information and save dataframe ####
    print('removing side info and saving into text file')
    if on=='phoneme':
        item = final[final["#phoneme"] != "+LAUGH+"]
        item = item[item["#phoneme"] != "SIL"]
        item = item[item["#phoneme"] != "+NOISE+"]
        item = item[item["#phoneme"] != "+BREATH+"]
        item = item[item["#phoneme"] != "+HUMAN+"]
        item.to_csv( output_dir+ "phoneme.item", sep='\t', header=True, index=False )
    elif on=='speakerID':
        item = final[final["phoneme"] != "+LAUGH+"]
        item = item[item["phoneme"] != "SIL"]
        item = item[item["phoneme"] != "+NOISE+"]
        item = item[item["phoneme"] != "+BREATH+"]
        item = item[item["phoneme"] != "+HUMAN+"]
        item.to_csv( output_dir+ "speakerID.item", sep='\t', header=True, index=False)
    elif on=='word':
        item = final[final["#word"] != "+LAUGH+"]
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
    '-d', '--dataset_type', type=str, metavar='<int>', default="test",
    help='type of dataset, either train, dev or test, default is %(default)s.')
    
parser.add_argument(
    '-pw', '--path_wav_spk_datasetype', type=str, 
    help='''path of the dircetory in which the file will be stored''')


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
   
    get_item_file(args.path_alignment, args.dataset_type, args.path_wav_spk_datasetype, args.output_dir , args.on, args.phone_alignment)
    

######### TERMINAL command

#python generate_item_file_flickr.py -p '/pylon5/ci560op/larsene/abx/flickr/flickr_labels/' -d 'test' -pw '/pylon5/ci560op/larsene/abx/flickr/df_wav_spk_set.txt' -o '/pylon5/ci560op/larsene/abx/flickr/test/mfcc/' --on 'phoneme' -a 'False'

##########   
    