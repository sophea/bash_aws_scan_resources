#!/usr/bin/env bash



regions="ap-southeast-1 us-east-1"
# Iterate the string variable using for loop
for item in $regions; do
 echo "====================image-scanning-configuration============"

aws ecr put-image-scanning-configuration \
	--region $item \
	--repository-name xxxxxxst-1 \
	--image-scanning-configuration scanOnPush=true


done




