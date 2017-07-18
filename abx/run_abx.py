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



input_folder= raw_input('Folder name containing the item file AND mfcc is ...')
ON=raw_input('the abx task is run on ...')
feature=raw_input('feature file name is ...')
ACROSS=raw_input('the abx task is done across ...')
BY=raw_input('the abx task is done by ...')

NB_CPU=raw_input("number of cpu to run the task on ")

out='/'+ 'on_'+ ON + '_by_' + BY + '_ac_'+ACROSS

out='/'+ 'on_'+ ON[0:2]+ '_by_' + BY[0:2]+BY[-2:] +'_ac_'+ACROSS[0:2]+ACROSS[-2:]

output_folder=input_folder + out


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


    # running the evaluation:
   
    if not os.path.exists(taskfilename):
        if ACROSS == "" and BY!="":
             task = ABXpy.task.Task(item_file,ON, by=BY)
             
        elif BY == "" and ACROSS!="":
             task = ABXpy.task.Task(item_file,ON, across=ACROSS)
             
        elif ACROSS =="" and BY == "" :
             task = ABXpy.task.Task(item_file,ON)
             
        else:
            task = ABXpy.task.Task(item_file,ON, across=ACROSS, by=BY)
             
    task.generate_triplets(taskfilename)
    stats=task.compute_statistics()
    try: 
        print(stats)
    except:
        pass
    
    print("Task is done")
    
    distances.compute_distances(feature_file, taskfilename,
                                distance_file, dtw_cosine_distance,
                                normalized = True, n_cpu=NB_CPU)
    print("Computing cosine distance is done")
                                
    score.score(taskfilename, distance_file, scorefilename)
    print("Score is computed")
    
    analyze.analyze(taskfilename, scorefilename, analyzefilename)
    print("Results are available in the csv file !!")


fullrun()

