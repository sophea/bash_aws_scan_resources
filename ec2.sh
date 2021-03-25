#!/usr/bin/env bash
source ./utils.sh
echo "====================EC2 Instances running======="
#running state value 16
aws ec2 describe-instances \
   --filters Name=instance-state-code,Values=16 \
    --query 'Reservations[*].Instances[*].{Instance:InstanceId,InstanceType:InstanceType,State:State.Name,Name:Tags[?Key==`Name`]|[0].Value}' \
    --output table

echo "====================EC2 Instances Stopped======="
##stopped instance state value 80
aws ec2 describe-instances    --filters Name=instance-state-code,Values=80     --query 'Reservations[*].Instances[*].{Instance:InstanceId,InstanceType:InstanceType,State:State.Name,Name:Tags[?Key==`Name`]|[0].Value}'     --output table



##find last lunchTime >= 30days
EC2_INSTANCES=($(aws ec2 describe-instances \
                    --filters Name=instance-state-code,Values=16 \
                    --query 'Reservations[*].Instances[*].{Instance:InstanceId,InstanceType:InstanceType,State:State.Name,Name:Tags[?Key==`Name`]|[0].Value,LaunchTime:LaunchTime}' \
    | jq '.[] | .[] | {Instance: .Instance, Name: .Name, InstanceType: .InstanceType,State: .State,  LaunchTime:.LaunchTime } | join("#") ' | tr -d '[]," '| tr -d '\r'))


now="$(date +'%m/%d/%Y %H:%M:%S')"

echo "====================Found old EC2 instances running more than 90days======="

for item in ${EC2_INSTANCES[@]}
do

    id=$(echo $item |  awk '{split($0,a,"#"); print a[1]}')
    name=$(echo $item |  awk '{split($0,a,"#"); print a[2]}')
	type=$(echo $item |  awk '{split($0,a,"#"); print a[3]}')
	state=$(echo $item |  awk '{split($0,a,"#"); print a[4]}')
	modifyDate=$(echo $item |  awk '{split($0,a,"#"); print a[5]}')
	age=$(dateDiff -d "$modifyDate" "$now")

	#(Last modified: 2 years ago, python3.6)

	if ((age > 90)); then
		last_started="(started $(($age/30)) months ago)"
		#echo "$id - $name - $type - $last_started"
		 printf "%-25s | %-15s | %-10s | %s\n" "$id" "$name" "$type" "$last_started"

	fi

done