# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 14:13:43 2017

@author: elinlarsen

This test contains a full run of the ABX pipeline
"""
# -*- coding: utf-8 -*-

import os
import argparse
import ABXpy.task
import ABXpy.distances.distances as distances
import ABXpy.distances.metrics.cosine as cosine
import ABXpy.distances.metrics.dtw as dtw
import ABXpy.score as score
import ABXpy.analyze as analyze



def dtw_cosine_distance(x, y, normalized):
    return dtw.dtw(x, y, cosine.cosine_distance, normalized)


def fullrun():
    
    if type(BY)==list:
        out='/'+ 'on_'+ ON[0:2]+ '_by_' + BY[0][0:2]+ '_'+ BY[1][0:2] +'_ac_'+ACROSS[0:2]
    else:
        out='/'+ 'on_'+ ON[0:2]+ '_by_' + BY[0:2] +'_ac_'+ACROSS[0:2]
    output_folder=input_folder + out


    print("the input folder is " + input_folder)
    print("the ABX task id done :" + out)    
    
    
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
        if ACROSS == "na" and BY!="na":
            task = ABXpy.task.Task(item_file,ON, by=BY)
             
        elif BY == "na" and ACROSS!="na":
            task = ABXpy.task.Task(item_file,ON, across=ACROSS)
             
        elif ACROSS =="na" and BY == "na" :
            task = ABXpy.task.Task(item_file,ON)
             
        else:
            task = ABXpy.task.Task(item_file,ON, across=ACROSS, by=BY)
            
        task.generate_triplets(taskfilename)

        try:
            task.print_stats(statsfilename)
        except:
            pass
    print("Task is done")
    
    print( "number of cpu used is " + str(NB_CPU))
    if not os.path.exists(distance_file):
        distances.compute_distances(feature_file, '/features/', taskfilename,
        	                         distance_file, dtw_cosine_distance,
                	                   normalized = True, n_cpu=NB_CPU)
    print("Computing cosine distance is done")
                                
    score.score(taskfilename, distance_file, scorefilename)
    print("Score is computed")
    
    analyze.analyze(taskfilename, scorefilename, analyzefilename)
    print("Results are available in the csv file !!")





parser = argparse.ArgumentParser(description='Run several abx task either on phone or word')


parser.add_argument(
    '--on', type=str, metavar='<str>', default="phoneme",
    help='either phoneme or word, default is %(default)s')

parser.add_argument(
    '-i', '--input', type=str, 
    help='path of the input folder containing the item file')

parser.add_argument(
     '-f', '--feature_file', type=list, default="mfcc.h5f",
     help='''name of the h5 file containing the acoustic features, default is %(default)s.''')

parser.add_argument(
     '--cpu', type=int, default=1,
     help='''number of CPU to run the task on, default is %(default)s ''')



if __name__=='__main__':
    """Entry point of the 'run_abx.py' command"""
    
    args=parser.parse_args()

    
    if args.on=="phoneme":
        d={"speakerID":"context",
	   "context":"speakerID",
	   "na":["speakerID", "context"]}
    
        for ACROSS, BY in d.iteritems():
            ON=args.on
            input_folder=args.input
            feature=args.feature_file
            NB_CPU=args.cpu
            fullrun()


    elif args.on=="word":
        d={"speakerID":"na",
           "na":"speakerID"}
        for ACROSS, BY in d.iteritems():
            ON=args.on
            input_folder=args.input
            feature=args.feature_file
            NB_CPU=args.cp
            fullrun()
