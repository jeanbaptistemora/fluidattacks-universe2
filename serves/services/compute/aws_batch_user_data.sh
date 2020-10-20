#!/bin/bash
#cloud-boothook

cloud-init-per once docker_options \
echo 'OPTIONS="${OPTIONS} --storage-opt dm.basesize=20G"' \
>> /etc/sysconfig/docker

{
  echo ECS_CONTAINER_START_TIMEOUT=60m
  echo ECS_ENABLE_SPOT_INSTANCE_DRAINING=true
  echo ECS_ENGINE_TASK_CLEANUP_WAIT_DURATION=1m
  echo ECS_IMAGE_CLEANUP_INTERVAL=10m
  echo ECS_IMAGE_MINIMUM_CLEANUP_AGE=1m
  echo ECS_IMAGE_PULL_BEHAVIOR=always
  echo ECS_IMAGE_PULL_INACTIVITY_TIMEOUT=60m
  echo ECS_NUM_IMAGES_DELETE_PER_CYCLE=100
  echo NON_ECS_IMAGE_MINIMUM_CLEANUP_AGE=1m
}  >> /etc/ecs/ecs.config
