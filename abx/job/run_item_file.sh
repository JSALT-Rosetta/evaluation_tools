#!/bin/bash
#SBATCH -N 10
#SBATCH -t 2:00:00
#echo commands to stdout

set - x

cd /pylon5/ci560op/larsene/evaluation_tools/abx/
source activate elin

#echo "create an item file "

S="/pylon2/ci560op/odette/data/mscoco/val2014/val_2014.sqlite3"
T="/pylon2/ci560op/odette/data/mscoco/val2014/tra/val_translate.sqlite3"
O="/pylon5/ci560op/larsene/abx/mscoco/test/"
ON="phoneme"

python generate_item_file.py  -s $S -t $T -o$O --on $ON 

echo "done"

