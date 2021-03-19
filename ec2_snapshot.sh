#!/usr/bin/env bash

SNAPSHOT_NO_VOLUMES=()
SNAPSHOT_VOLUMES=($(aws ec2 describe-snapshots --owner-ids self | jq '.Snapshots[] | {SnapshotId: .SnapshotId, VolumeId: .VolumeId} | join("  - ") ' | tr -d '[]," '| tr -d '\r'))

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
aws ec2 describe-snapshots --owner-ids self | jq '.Snapshots[] | {SnapshotId: .SnapshotId, Description: .Description} | join("  - ") '  | grep  -v 'ami' 

