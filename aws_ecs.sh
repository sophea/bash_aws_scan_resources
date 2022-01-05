#!/usr/bin/env bash

echo "======================AWS ECS =========="
## --output table text json
aws ecs list-clusters --output table


echo "======================AWS ECR Repositories =========="
## --output table text json
aws ecr	 describe-repositories --output table