#!/usr/bin/env bash


echo "======================APIGETWAY=========="

aws apigateway get-rest-apis | jq '.items[] | {name: ("name:" + .name), type : ("types:" + (.endpointConfiguration.types|join(" ; ")))}  | join ("|")' | tr -d '[],"'| tr -d '\r'

#API_GW_LIST = $(aws apigateway get-rest-apis | jq '.items[] | {name: .name, type : .endpointConfiguration.types|join(";") } | join ("##")' | tr -d '[],"'| tr -d '\r')
#for api in $API_GW_LIST
#do
	
#done

