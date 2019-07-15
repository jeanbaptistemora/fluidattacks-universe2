#!/usr/bin/env bash

# This scripts checks whether the docker image was changed and pushes it
# to the registry if the branch is master

echo "{\"auths\":{\"${CI_REGISTRY}\":{\"username\":\"${CI_REGISTRY_USER}\",\
  \"password\":\"${CI_REGISTRY_PASSWORD}\"}}}" > /root/.docker/config.json

if [[ "$CI_COMMIT_REF_NAME" == "master" ]]; then
  /kaniko/executor \
    --context "${CI_PROJECT_DIR}" \
    --dockerfile "deploy/containers/$1/Dockerfile" \
    --destination "${CI_REGISTRY_IMAGE}:$1" \
    --cache=true \
    --cache-repo "${CI_REGISTRY_IMAGE}/cache/$1" \
    --snapshotMode time
else
  /kaniko/executor \
    --context "${CI_PROJECT_DIR}" \
    --dockerfile "deploy/containers/$1/Dockerfile" \
    --no-push \
    --cache=true \
    --cache-repo "${CI_REGISTRY_IMAGE}/cache/$1" \
    --snapshotMode time
fi
