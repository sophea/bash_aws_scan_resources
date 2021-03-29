#!/usr/bin/env bash
source ./utils.sh

SNAPSHOT_NO_VOLUMES=()
SNAPSHOT_VOLUMES=($(aws ec2 describe-snapshots --owner-ids self | jq '.Snapshots[] | {SnapshotId: .SnapshotId, VolumeId: .VolumeId} | join("  - ") ' | tr -d '[],"'| tr -d '\r'))

echo "====================${#SNAPSHOT_VOLUMES[@]} snapshots found======="

ALL_VOLUMES=($(aws ec2 describe-volumes --query 'Volumes[].{ID: VolumeId}' --output text | tr -d '\r'))
#ALL_VOLUMES+=("vol-088f5020af822f92a")
for sv in "${SNAPSHOT_VOLUMES[@]}"
do
    value="";
    for v in "${ALL_VOLUMES[@]}"
    do
        #case "${SNAPSHOT_VOLUMES[@]}" in  *"${sv}"*) echo "found" ;; esac
        #value=$(array_contains  SNAPSHOT_VOLUMES  "$v")
        if [[ "$sv" == *"$v"* ]] ; then
            value="$sv"
            break;
        fi
    done
    if [[ ! -z "$value" ]]; then
        SNAPSHOT_NO_VOLUMES+=("$value")
    fi
done
echo "====================${#SNAPSHOT_NO_VOLUMES[@]} snapshots exist for non-existing volumes:======="
for v in "${SNAPSHOT_NO_VOLUMES[@]}"
do
    echo "  - $v "
done

###Snaphosts
echo "=========Unused Snaphosts- (no ami attached)========="
aws ec2 describe-snapshots --owner-ids self | jq '.Snapshots[] | {SnapshotId: .SnapshotId, Description: .Description} | join(" - ") '  | grep  -v 'ami'


###Snaphosts
echo "=========Snaphosts- older than 90days========="
SNAPSHOT=($(aws ec2 describe-snapshots --owner-ids self | jq '.Snapshots[] | {SnapshotId: .SnapshotId, Description: .Description, StartTime: .StartTime} | join("#")' | tr -d '[]," '| tr -d '\r'))

now="$(date +'%m/%d/%Y %H:%M:%S')"

for item in ${SNAPSHOT[@]}
do
	#echo $item

	id=$(echo $item |  awk '{split($0,a,"#"); print a[1]}')
	description=$(echo $item |  awk '{split($0,a,"#"); print a[2]}')
	startTime=$(echo $item |  awk '{split($0,a,"#"); print a[3]}')
	age=$(dateDiff -d "$startTime" "$now")


	if ((age > 90)); then
		last_started="(created $(($age/30)) months ago)"
		#echo "$id - $name - $type - $last_started"
		 printf "%-25s | %-100s | %s\n" "$id" "${description:0:98}" "$last_started"

	fi
done