#!/usr/bin/env bash

BADSTACKS=""
STOPPEDSTACKS=""

echo "======================cloudformation=========="


for STACK in $(aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --max-items 1000 | jq -r '.StackSummaries[].StackName' | tr -d '\r')
do
        INSTANCE=$(aws cloudformation describe-stack-resources --stack-name $STACK | jq -r '.StackResources[] | select (.ResourceType=="AWS::EC2::Instance")|.PhysicalResourceId')
        if [[ ! -z $INSTANCE  ]]; then
                STATUS=$(aws ec2 describe-instance-status --include-all-instances --instance-ids $INSTANCE 2> /dev/null | jq -r '.InstanceStatuses[].InstanceState.Name') 
                if [[ -z $STATUS  ]]; then
                        BADSTACKS="${BADSTACKS:+$BADSTACKS }$STACK"
                elif [[ ${STATUS} == "stopped" ]]; then
                        STOPPEDSTACKS="${STOPPEDSTACKS:+$STOPPEDSTACKS }$STACK"
				fi
        fi
		echo " - $STACK"
done
echo "====Finding misconfigured AWS assets, stand by..."
echo "==CloudFormation stacks with missing EC2 instances: (aws cloudformation delete-stack --stack-name)"
echo " - $BADSTACKS "
echo "==CloudFormation stacks with stopped EC2 instances: (aws cloudformation delete-stack --stack-name)"
echo " - $STOPPEDSTACKS  "

