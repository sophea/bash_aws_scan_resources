#!/usr/bin/env bash
# 
# ---------------------
start_time="$(date +%s%N)"


#param as second
function displaytime {
  local T=$1
  local D=$((T/60/60/24))
  local H=$((T/60/60%24))
  local M=$((T/60%60))
  local S=$((T%60))
  (( $D > 0 )) && printf '%d days ' $D
  (( $H > 0 )) && printf '%d hours ' $H
  (( $M > 0 )) && printf '%d minutes ' $M
  (( $D > 0 || $H > 0 || $M > 0 )) && printf 'and '
  printf '%d seconds\n' $S
}

DATE="$(date +'%d-%m-%Y')"

CURRENT_DIR=`dirname "$0"`
cd $CURRENT_DIR


S3_BUCKET_NAME="s3://jtrust-datamigration-uat/test"
S3_LIST_FILE="s3.txt"
OUT_PUT_RESULT_FILE="result-${DATE}.txt"
OUT_PUT_FAILED_FILE="failure-${DATE}.txt"

echo "Read file $S3_LIST_FILE"
if [[ ! -s $S3_LIST_FILE ]]; then
    echo "The file $S3_LIST_FILE is not found"
    exit 1
fi
##empty file
echo ""> $OUT_PUT_RESULT_FILE
echo ""> $OUT_PUT_FAILED_FILE

success_count=0
failure_count=0
##read line by line
while read line; do
    KEY="${S3_BUCKET_NAME}/$line"
    aws s3 ls "$KEY"
    if [[ $? -ne 0 ]]; then
        echo "File does not exist:$KEY" >> $OUT_PUT_FAILED_FILE
		failure_count=$((failure_count+1))
    else
		success_count=$((success_count+1))
        aws s3 rm "$KEY"
        echo "removed:$KEY" >> $OUT_PUT_RESULT_FILE
    fi
done < $S3_LIST_FILE

#success_count=$(cat $OUT_PUT_RESULT_FILE | sed '/^\s*$/d' | wc -l)
echo "Delete S3 resources - please check the result"
echo "---- Number of failure : $failure_count" 
echo "---- Number of success : $success_count" 

################elapsed time process############3
end_time="$(date +%s%N)"
elapsed="$((($end_time-$start_time)/1000000/1000))"
value=$(displaytime ${elapsed})
echo -e "\n\n--------------------------------"
echo "Total of $value elapsed for the process"
echo -e "------------------------------------"
