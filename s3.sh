#!/usr/bin/env bash
# ---------------------
echo "==============S3 buckets==============="

ALL_S3=($(aws s3api list-buckets --query "Buckets[].Name" | jq -r '.[]' | tr -d '\r'))
echo " Found ${#ALL_S3[@]}  S3 buckets"
echo " =========S3 buckets are empty========"
for item in "${ALL_S3[@]}"
do
    size=$(aws s3api list-objects-v2 --bucket $item --max-items 1| jq -r '.Contents[0] | {size:.Size} | .[]')
    if [[ -z "$size" ]]; then
        echo " - $item - (empty) "
    fi
done

