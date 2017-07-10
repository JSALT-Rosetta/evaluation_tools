#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 17:18:26 2017

@author: elinlarsen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
    


def autolabel(rects, ax):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')
        
        

def count_occurrences(item_file, occ_of, name_fig="occurence_in_file", the_n_first=50, log_scale=True): 
    """
    Count the number of occurrences of "occ_of" in the item file
    Parameters
    ----------
    item file : text file or dataframe containing at least as columns :  onset, offset, 
        #phoneme and context and side information such as image ID
    occ_of : string,
         Example : "phoneme " word" 
    name_fig : string,    
         number of values of 'col' to get from the sampling,
    the_n_first: string, 
        the first n of "occ_of"
    log_scale: Bool, 
        whether or not the scale is logarithm  defaut=True
    """
    
    try : 
    
        if isinstance(item_file,str):
            #open item file
            df=pd.read_csv(item_file, sep='\t')
            
        elif isinstance(item_file,pd.core.frame.DataFrame): 
            df=item_file
    
    except ValueError: 
        print ("item_file must be a path (string) or a dataframe")
        
    #drop empty column
    try : 
        df.drop('Unnamed: 0', axis=1, inplace=True)
    except :
        pass
        
    counts= df.groupby("".join(["#", occ_of])).count()[[0]]
    counts.columns=['count']
    counts.sort_values(by='count',axis=0, ascending=False, inplace=True)
    
    counts_truncated=counts[0:the_n_first]
    
    
    fig=plt.figure(figsize=(15.0, 10.0))
    ax=plt.axes()
    x=counts_truncated.index.values.tolist()
    y=counts_truncated['count'].tolist()
    N = len(counts_truncated)
    width=0.5
    # the width of the bars

    rects = ax.bar(range(N), y, width, log=log_scale)
    
    ax.set_ylabel('Number of occurrences')
    ax.set_xticks(range(N))
    ax.set_xticklabels(x)
    
    autolabel(rects,ax)
    
    plt.show()
    my_path = os.path.abspath(item_file) 
    fig.savefig(os.path.join(my_path, name_fig))   
    
    
def histogram(item_file, col1, col2, name_fig): 
    """
    Sample an item file to get a reasonable size for running an ABX task
    Parameters
    ----------
    item file : text file containing at least as columns :  onset, offset, 
    #phoneme and context and side information such as image ID, speakerID
    col1 : string,
         name of the column of the item file in which the distrbition on col2 will
         be looked on. Example : speakerID, speaker_nationality
    col2: str,    
         number of the column that will be the exis of the histogram. 
         Example : imageID, captionID
    name_fig: str,
         name of the figure 
    """
    
    try : 
    
        if isinstance(item_file,str):
            #open item file
            df=pd.read_csv(item_file, sep='\t')
            
        elif isinstance(item_file,pd.core.frame.DataFrame): 
            df=item_file
    
    except ValueError: 
        print ("item_file must be a path (string) or a dataframe")
    
    
    # get the histogram 
    fig, ax = plt.subplots()
    df[[col1, col2]].hist(by=col1,ax=ax)

    my_path = os.path.abspath(item_file) 
    fig.savefig(os.path.join(my_path, name_fig)) 
    
    
#test
#item_file="/Users/elinlarsen/Documents/2017_JSALT/results/mscoco/val2014/word.item"

#test_w=random_sampling(item_file, group_by='imageID', sample_size=5000, replace=False)
#test_w.columns=["#file_name", "onset", "offset", "#word", "imageID", "captionID", "speakerID", "speaker_nationality", "null"]
#count_occurrences(test_w, "word", "count_word_log", 50, True)



   
    
    