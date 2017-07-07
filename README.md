# evaluation_tools
Intrinsic and extrinsic evaluation metrics

Starting with ABX tasks

_______
script : item_data_mscoco.py

Create a data file "XX.item" for an ABX task on XX
Requirement : the speechcoco package need to be installed
Can be run on terminal.
Example as follow :
SOURCE="/pylon2/ci560op/odette/data/mscoco/val2014/val_2014.sqlite3"
TARGET="/pylon2/ci560op/odette/data/mscoco/val2014/tra/val_translate.sqlite3"     
OUT="/pylon2/ci560op/larsene/abx_eval/mscoco/val2014/ »
ON="phoneme"
NAMES="["#file_name", "onset", "offset", "#phoneme", "context", "imageID", "captionID", "speakerID", "speaker_nationality"]"
ALIGN="False"


python item_data_mscoco.py -s  $SOURCE -t $TARGET -o $OUT --on $ON -n $NAMES -a $ALIGN
