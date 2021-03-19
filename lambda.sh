#!/usr/bin/env bash

source ./utils.sh

echo "======================LambdaFunctions=========="

LAMBDA_FUNCTION=$(aws lambda list-functions | jq -r '.Functions[] | {name: .FunctionName, Runtime: .Runtime , MemorySize: .MemorySize|tostring, LastModified: .LastModified} | join ("#")' | tr -d '\r')

now="$(date +'%m/%d/%Y %H:%M:%S')"

for item in $LAMBDA_FUNCTION
do
	#echo $item
	
	name=$(echo $item |  awk '{split($0,a,"#"); print a[1]}')
	runtime=$(echo $item |  awk '{split($0,a,"#"); print a[2]}')
	size=$(echo $item |  awk '{split($0,a,"#"); print a[3]}')
	modifyDate=$(echo $item |  awk '{split($0,a,"#"); print a[4]}')
	age=$(dateDiff -d "$modifyDate" "$now")
	
	#(Last modified: 2 years ago, python3.6)
	
	if ((age > 90)); then
		echo "$name - MemorySize $size MB - (Last modify $(($age/30)) months ago , $runtime )"
	else
		echo "$name - MemorySize $size MB - (Last modify $(($age/30)) days ago , $runtime )"
	fi
done

