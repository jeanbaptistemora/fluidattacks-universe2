#!/bin/bash

docker stop integrates
docker rm integrates
rm -f ~/.ssh/config.facont
rm -f ~/.ssh/facont_id_rsa*

