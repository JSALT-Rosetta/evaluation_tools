#!/bin/bash
set=$1
unit=$2

for s in "$set"
do
for u in "$unit"
do 

python select_rows_in_item_file.py -i  /pylon5/ci560op/larsene/abx/mscoco/"$s"/"$u".item -w /pylon2/ci560op/odette/data/8K_mscoco/"$s"/wav/wave_file_names.txt -o /pylon5/ci560op/larsene/abx/8K_mscoco/"$s"/"$u".item

echo set "$s" done
done
echo unit "$u" done
done
