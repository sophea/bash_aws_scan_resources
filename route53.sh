#!/usr/bin/env bash
echo "====================ROUTE53==========="
ROUTE53=$(aws route53 list-hosted-zones | jq '.HostedZones[] | {Name: .Name, Config: .Config.PrivateZone|tostring, ResourceRecordSetCount: .ResourceRecordSetCount|tostring } | join("#") ' | tr -d '[]," '| tr -d '\r')
for item in $ROUTE53
do
    name=$(echo $item |  awk '{split($0,a,"#"); print a[1]}')
    type=$(echo $item |  awk '{split($0,a,"#"); print a[2]}')
    records=$(echo $item |  awk '{split($0,a,"#"); print a[3]}')
    typeValue="private"
    if [[ $type == true ]]; then
        typeValue="public"
    fi
    printf "%-20s type:%-8s records:%3d\n" $name $typeValue $records

   # echo " name: $name , type: $typeValue , records : $records"
    
done
