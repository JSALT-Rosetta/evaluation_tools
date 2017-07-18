# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 14:13:43 2017

@author: elinlarsen

This test contains a full run of the ABX pipeline
"""
# -*- coding: utf-8 -*-

import os
import sys
package_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if not(package_path in sys.path):
    sys.path.append(package_path)
import ABXpy.task
import ABXpy.distances.distances as distances
import ABXpy.distances.metrics.cosine as cosine
import ABXpy.distances.metrics.dtw as dtw
import ABXpy.score as score
import ABXpy.analyze as analyze





def dtw_cosine_distance(x, y, normalized):
    return dtw.dtw(x, y, cosine.cosine_distance, normalized)



def fullrun():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    item_file = input_folder+'/' + ON+'.item'
    feature_file = input_folder+'/'+ feature
    distance_file = output_folder+ '/'+out + '.distance'
    scorefilename = output_folder+'/'+ out +'.score'
    taskfilename = output_folder + '/'+out +'.abx'
    analyzefilename = output_folder + '/'+out + '.csv'
    statsfilename=output_folder + '/'+out + '.stats'


    # running the evaluation:
   
    if not os.path.exists(taskfilename):
        if ACROSS == "NaN" and BY!="NaN":
             task = ABXpy.task.Task(item_file,ON[i], by=BY[b])
             
        elif BY == "NaN" and ACROSS!="NaN":
             task = ABXpy.task.Task(item_file,ON[i], across=ACROSS[a])
             
        elif ACROSS =="NaN" and BY == "NaN" :
             task = ABXpy.task.Task(item_file,ON[i])
             
        else:
            task = ABXpy.task.Task(item_file,ON[i], across=ACROSS[a], by=BY[b])
            
        task.generate_triplets(taskfilename)
        task.print_stats(statsfilename)
    print("Task is done")
    
    print( "number of cpu used is" + str(NB_CPU))
    if not os.path.exists(distance_file):
	    distances.compute_distances(feature_file, '/features/', taskfilename,
        	                        distance_file, dtw_cosine_distance,
                	                normalized = True, n_cpu=NB_CPU)
    print("Computing cosine distance is done")
                                
    score.score(taskfilename, distance_file, scorefilename)
    print("Score is computed")
    
    analyze.analyze(taskfilename, scorefilename, analyzefilename)
    print("Results are available in the csv file !!")


DATASET="test/tests/"
input_folder= "pylon2/ci560op/odette/data/abx/8K_mscoco/"+DATASET
feature="mfcc.h5f"
NB_CPU=1

'''
ON="phoneme"
    for b in BY:
        for a in ACROSS:
            out='/'+ 'on_'+ ON[0:2]+ '_by_' + BY[0:2]+BY[-2:] +'_ac_'+ACROSS[0:2]+ACROSS[-2:]
            output_folder=input_folder + out
            fullrun()
'''     
      
ON="word"
ACROSS="speakerID"
BY="NaN"
out='/'+ 'on_'+ ON[0:2]+ '_by_' + BY[0:2]+BY[-2:] +'_ac_'+ACROSS[0:2]+ACROSS[-2:]
output_folder=input_folder + out
fullrun()

'''
ON="word"
BY="speakerID"
ACROSS="NaN"
out='/'+ 'on_'+ ON[0:2]+ '_by_' + BY[0:2]+BY[-2:] +'_ac_'+ACROSS[0:2]+ACROSS[-2:]
output_folder=input_folder + out
fullrun()
'''
