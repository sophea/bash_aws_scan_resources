#!/usr/bin/env bash



regions="ap-northeast-1 ap-northeast-2 ap-northeast-3 ap-south-1 ap-southeast-1 ap-southeast-2 ca-central-1 eu-central-1 eu-north-1 eu-west-1 eu-west-2 eu-west-3 sa-east-1 us-east-1 us-east-2 us-west-1 us-west-2"

# Iterate the string variable using for loop
for item in $regions; do
 echo "======================SET EBS Encryption : region ${item}=========="
 aws ec2 enable-ebs-encryption-by-default --region $item
done
