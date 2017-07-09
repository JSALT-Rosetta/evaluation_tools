# evaluation_tools
Intrinsic and extrinsic evaluation metrics

Starting with ABX tasks

_______
<br >Script : item_data_mscoco.py <br />

<br >Requirement : the speechcoco package need to be installed <br />
<br >Can be run on terminal.<br />
<br >Example as follow :<br />
<br >SOURCE="/pylon2/ci560op/odette/data/mscoco/val2014/val_2014.sqlite3"<br />
<br >TARGET="/pylon2/ci560op/odette/data/mscoco/val2014/tra/val_translate.sqlite3"    <br />
<br >OUT="/pylon2/ci560op/larsene/abx_eval/mscoco/val2014/ »<br />
<br >ON="phoneme"<br />
<br >NAMES="["#file_name", "onset", "offset", "#phoneme", "context", "imageID", "captionID", "speakerID", "speaker_nationality"]" <br />
<br >ALIGN="False"<br />


<br >python item_data_mscoco.py -s  $SOURCE -t $TARGET -o $OUT --on $ON -n $NAMES -a $ALIGN <br />
