#!/bin/bash

cd "/scripts"

services=$(ls services/)
for service in $services
do
    objects=$(ls  services/$service/)

    for object in $objects
    do
        python3 "services/$service/$object"
    done
done