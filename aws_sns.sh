#!/usr/bin/env bash

echo "======================AWS SNS Topics =========="
## --output table text json
aws sns list-topics --output table
