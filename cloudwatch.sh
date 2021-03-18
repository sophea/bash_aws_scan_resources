#!/usr/bin/env bash
# ---------------------
echo "==============Cloudwatch==============="
aws logs describe-log-groups | jq -r '.logGroups[] | select(.retentionInDays<0) | {name:.logGroupName, retentionInDays: ("  Expire: Never") , size: (.storedBytes|tostring + " bytes")} | join(" - ")' 


aws logs describe-log-groups | jq -r '.logGroups[] | select(.retentionInDays>0) | {name:.logGroupName, retentionInDays: (.retentionInDays|tostring + " days") , size: (.storedBytes|tostring + " bytes")} | join(" - ")' 

