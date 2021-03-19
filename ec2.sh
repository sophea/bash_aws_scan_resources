#!/usr/bin/env bash
echo "====================EC2 Instances running======="
#running state value 16
aws ec2 describe-instances \
   --filters Name=instance-state-code,Values=16 \
    --query 'Reservations[*].Instances[*].{Instance:InstanceId,InstanceType:InstanceType,State:State.Name,Name:Tags[?Key==`Name`]|[0].Value}' \
    --output table

echo "====================EC2 Instances Stopped======="
##stopped instance state value 80
aws ec2 describe-instances    --filters Name=instance-state-code,Values=80     --query 'Reservations[*].Instances[*].{Instance:InstanceId,InstanceType:InstanceType,State:State.Name,Name:Tags[?Key==`Name`]|[0].Value}'     --output table








