#!/usr/bin/env python
#
# Copyright 2016, 2017 Elin Larsen, Julien Karadyi
#
# You can redistribute this file and/or modify it under the terms of
# the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""Evaluation program for ABX task done  :
    - on phoneme across speaker by context ("across")
    - on phoneme across context by speaker ("within")
    - on phoneme by context and by speaker ("control")
    
    - on word by speaker ("within")
    - on word across speaker ("across")
    
    - on speaker across phoneme by context

"""

import argparse
import numpy as np
import pandas
import os

def avg(filename, output_dir, on='phoneme', across='speakerID', ponderate=False):
    input_folder=os.path.dirname(os.path.abspath(filename))
    df = pandas.read_csv(filename, sep='\t', header=0)
    
    if on=="phoneme":
        df = df[df.phoneme_1!= '#']
        df = df[df.phoneme_2!= '#']
        df = df[df.phoneme_1!= '__#__']
        df = df[df.phoneme_2!= '__#__']
    
        if across == 'speakerID':
            groups = df.groupby(['speakerID_1', 'speakerID_2', 'phoneme_1', 'phoneme_2'], as_index=False)
            if ponderate:
                average=groups.apply(lambda x: np.average(x.score, weights=x.n))
            else:
                average=groups.apply(lambda x: np.average(x.score, weights=None))
            res_per_speaker=average.mean(level="speakerID_1")    
            res_per_unit=average.mean(level="phoneme_1")
            res_per_context=0
        
        
        elif across == 'context':

            groups = df.groupby(['phoneme_1', 'phoneme_2', 'context_1', 'context_2'], as_index=False)
            if ponderate:
                average=groups.apply(lambda x: np.average(x.score, weights=x.n))
            else:
                average=groups.apply(lambda x: np.average(x.score, weights=None))
            res_per_speaker=0
            res_per_context=average.mean(level="context_1")    
            res_per_unit=average.mean(level="phoneme_1")

        

            
        elif across=='na':
            groups = df.groupby(['phoneme_1', 'phoneme_2', 'by'], as_index=False) 
            gp=df.groupby('by', as_index=False)
            by=gp.mean()
            list_of_by=[eval(b) for b in by.index]
            d=pandas.DataFrame(list_of_by, columns=['speakerID', 'context'])
            d['score']=list(by['score'])

            if ponderate:
                average=groups.apply(lambda x: np.average(x.score, weights=x.n))
            else:
                average=groups.apply(lambda x: np.average(x.score, weights=None))
            res_per_speaker=d.groupby('speakerID').mean()
            res_per_context=d.groupby('context').mean()['score']
            res_per_unit=average.mean(level="phoneme_1")

        
            
        else:
            raise ValueError('Unknown task type: {0}'.format(across))
      
      
    elif on=="speakerID":
        groups = df.groupby(['by', 'speakerID_1', 'speakerID_2'], as_index=False)
        if ponderate:
            average=groups.apply(lambda x: np.average(x.score, weights=x.n))
        else:
            average=groups.apply(lambda x: np.average(x.score, weights=None))
        res_per_speaker=average.mean(level="speakerID_1")    
        res_per_unit=average.mean(level="by")
        res_per_context=0
    
           
        
    elif on=="word":
    
        if across=='speakerID':
            groups = df.groupby(['speakerID_1', 'speakerID_2', 'word_1', 'word_2'], as_index=False)
            if ponderate:
                average=groups.apply(lambda x: np.average(x.score, weights=x.n))
            else:
                average=groups.apply(lambda x: np.average(x.score, weights=None))
            res_per_context=0
            res_per_speaker=average.mean(level="speakerID_1")    
            res_per_unit=average.mean(level="word_1")
        


        elif across=='na':
            groups = df.groupby(['word_1', 'word_2'], as_index=False)
            if ponderate:
                average=groups.apply(lambda x: np.average(x.score, weights=x.n))
            else:
                average=groups.apply(lambda x: np.average(x.score, weights=None))    
            res_per_unit=average.mean(level="word_1")
            res_per_context=0
            res_per_speaker=0

    
    res=average.mean()
    res_per_unit.to_csv(input_folder+'/score_per_unit.txt', sep='\t', header=0, index=True)
    
    if isinstance(res_per_speaker, int)==False:
        res_per_speaker.to_csv(input_folder+'/score_per_speaker.txt', sep="\t", header=0, index=True)
        
    if isinstance(res_per_context, int)==False:
        res_per_context.to_csv(input_folder+'/score_per_context', sep='\t', header=0, index=True)
    print(res)
    f=open(output_dir +"results_abx.txt", 'a')
    f.write (filename.split(".")[0] + "\t" + str(res) + "\n")
    return (res)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage="%(prog)s task distance [score]",
                                     description='ABX score computation')
                                     
    g1 = parser.add_argument_group('I/O files')
    
    g1.add_argument(
    '-f','--filename', type=str, metavar='<str>',  
    help='cvs file with the results for all pairs')
    
    g1.add_argument(
    '-o', '--output_dir', type=str, metavar='<str>',
    help='path of the directory where all ABX scores will be written on')
    
    g1.add_argument(
    '--on', type=str, metavar='<str>', default="phoneme",
    help='either phoneme,  word or speaker, default is %(default)s')
    
    g1.add_argument(
    '-t', '--across', type=str, metavar= '<str>', default= 'speakerID', 
    help='whether the ABX task is done across speakerID or context or na, default is %(default)s')
    
    g1.add_argument(
    '-p', '--ponderate', type=bool, default= False, 
    help='weight score on number of phoneme pairs or not , default is %(default)s')
    
    
    args = parser.parse_args()
    print("the ABX score of the task: " + args.filename.split('.')[0])
    avg(args.filename, args.output_dir, args.on, args.across, args.ponderate)
    


























































