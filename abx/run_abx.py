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



folder_name= raw_input('Folder name containing the item file is ...')
ON=raw_input('the abx task is run on ...')
feature=raw_input('feature file name is ...')
ACROSS=raw_input('the abx task is done across ...')
BY=raw_input('the abx task is done by ...')

out='/'+ 'on_'+ ON + '_by_' + BY + '_across_'+ACROSS



def dtw_cosine_distance(x, y, normalized):
    return dtw.dtw(x, y, cosine.cosine_distance, normalized)



def fullrun():
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    item_file = folder_name+'/' + ON+'.item'
    feature_file = folder_name+'/'+ feature
    distance_file = folder_name+ out + '.distance'
    scorefilename = folder_name+ out +'.score'
    taskfilename = folder_name + out +'.abx'
    analyzefilename = folder_name + out + '.csv'


    # running the evaluation:
   
    task = ABXpy.task.Task(item_file,ON, across=ACROSS, by=BY)
    task.generate_triplets(taskfilename)
    distances.compute_distances(feature_file, '/features/', taskfilename,
                                distance_file, dtw_cosine_distance,
                                normalized = True, n_cpu=1)
    score.score(taskfilename, distance_file, scorefilename)
    analyze.analyze(taskfilename, scorefilename, analyzefilename)


fullrun()
