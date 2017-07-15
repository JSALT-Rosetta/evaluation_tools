set=$1
unit=$2

for s in $set
do
for u in $unit
do 

python select_rows_in_item_file.py  -i  /pylon2/ci560op/larsene/abx_eval/mscoco/$s2014/$u.item -w /pylon2/ci560op/odette/data/8K_mscoco/$s/wav/wave_file_names.txt -o /pylon2/ci560op/odette/data/abx/8K_mscoco/$s/$u.item

echo set $s done
done
echo unit $u done
done
