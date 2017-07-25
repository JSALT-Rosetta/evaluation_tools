#!/usr/bin/env python
#
# Copyright 2016, 2017 Julien Karadyi
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
"""Evaluation program for the Zero Speech Challenge 2017

Track 1: Unsupervised subword modeling

"""

import ast
import argparse
import ConfigParser
import h5py
import os
import numpy as np
import pandas
import pickle
import sys
import warnings

from tables import DataTypeWarning
from tables import NaturalNameWarning

import ABXpy.distances.distances as distances
import ABXpy.distances.metrics.cosine as cosine
import ABXpy.distances.metrics.dtw as dtw
import ABXpy.score as score
import ABXpy.analyze as analyze
from ABXpy.misc import any2h5features

def lookup(attr, task_items, default=None):
    if attr in task_items:
        return task_items[attr]
    else:
        return default


def avg(filename, task_type='across'):
    #task_type = lookup('type', task, 'across')
    df = pandas.read_csv(filename, sep='\t')
    if task_type == 'across':
        # aggregate on context
        groups = df.groupby(
            ['speaker_1', 'speaker_2', 'phone_1', 'phone_2'], as_index=False)
        df = groups['score'].mean()
    elif task_type == 'within':
        arr = np.array(map(ast.literal_eval, df['by']))
        df['speaker']  = [e for e, f, g in arr]
        df['context'] = [f for e, f, g in arr]
        #del df['by']

        # aggregate on context
        groups = df.groupby(['phone_1', 'phone_2'], as_index=False) 
        #groups = df_within.groupby(['speaker', 'phone_1', 'phone_2'], as_index=False)
        df = groups['score'].mean()
    else:
        raise ValueError('Unknown task type: {0}'.format(task_type))

    # del df['by']
    # # aggregate on talkers
    # groups = df.groupby(['context', 'word_1', 'word_2'], as_index=False)
    # df = groups['score'].mean()
    # # aggregate on contexts
    # groups = df.groupby(['word_1', 'word_2'], as_index=False)
    # df = groups['score'].mean()
    
    ## Compute confidence interval with bootstrap method : 

    boot=df 
    n = 40000
    N = 1000

    ci=[]
    
    #for i in xrange(0,N):
    #    bt=boot.merge(pandas.DataFrame(index=np.random.randint(n, size=n)), left_index=True, right_index=True, how='right')
    #    groups=bt.groupby(['phone_1','phone_2'],as_index=False)
    #    bt=groups['score'].mean()
    #    average = bt.mean()[0]
    #    ci.append(average)
    #ci=sorted(ci)
    #confidence=[ci[int(round(0.5*N))],ci[int(round(0.95*N))]]
    confidence=[0,0]
    # aggregate on talker
    #groups = df.groupby(['phone_1', 'phone_2'], as_index=False)
    #df = groups['score'].mean()
    average = df.mean()[0]
    average = (1.0-average)*100
    return (average,confidence)


if __name__ == '__main__':

    import argparse

    # parser (the usage string is specified explicitly because the default
    # does not show that the mandatory arguments must come before the mandatory
    # ones; otherwise parsing is not possible beacause optional arguments can
    # have various numbers of inputs)
    parser = argparse.ArgumentParser(usage="%(prog)s task distance [score]",
                                     description='ABX score computation')
    # I/O files
    g1 = parser.add_argument_group('I/O files')
    g1.add_argument('filename', help='cvs file with the results for all pairs')
    g1.add_argument('task', help='across or within speakers')
    #g1.add_argument('score', help='output file for score')
    
    args = parser.parse_args()

    #if os.path.exists(args.score):
     #   print("Warning: overwriting score file {}".format(args.score))
      #  os.remove(args.score)
    

    print avg(args.filename,args.task)


























































