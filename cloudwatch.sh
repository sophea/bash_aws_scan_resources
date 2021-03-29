#!/usr/bin/env bash

source ./utils.sh
# ---------------------
echo "==============Cloudwatch (never expired)==============="
#aws logs describe-log-groups | jq -r '.logGroups[] | select(.retentionInDays<0) | {name:.logGroupName, retentionInDays: ("  Expire: Never") , size: (.storedBytes|tostring + " bytes")} | join(" - ")'
LOGS=($(aws logs describe-log-groups | jq -r '.logGroups[] | select(.retentionInDays<0) | {name:.logGroupName, retentionInDays: ("  Expire: Never")  , size: (.storedBytes|tostring)} | join("#")'  | tr -d '[]," '| tr -d '\r'))
for item in ${LOGS[@]}
do
	#echo $item
	name=$(echo $item |  awk '{split($0,a,"#"); print a[1]}')
	days=$(echo $item |  awk '{split($0,a,"#"); print a[2]}')
	size=$(echo $item |  awk '{split($0,a,"#"); print a[3]}')
	sizeAsValue=$(bytesToHumanReadable "$size")
	printf "%-50s | %-20s | %s\n" "${name:0:49}" "$days" "$sizeAsValue"

done




LOGS=($(aws logs describe-log-groups | jq -r '.logGroups[] | select(.retentionInDays>0) | {name:.logGroupName, retentionInDays: (.retentionInDays|tostring + " days") , size: (.storedBytes|tostring)} | join("#")'  | tr -d '[]," '| tr -d '\r'))
for item in ${LOGS[@]}
do
	#echo $item

	name=$(echo $item |  awk '{split($0,a,"#"); print a[1]}')
	days=$(echo $item |  awk '{split($0,a,"#"); print a[2]}')
	size=$(echo $item |  awk '{split($0,a,"#"); print a[3]}')
	sizeAsValue=$(bytesToHumanReadable "$size")
	printf "%-50s | %-20s | %s\n" "${name:0:49}" "$days" "$sizeAsValue"

done
