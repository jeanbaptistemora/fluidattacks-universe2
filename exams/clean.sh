#!/bin/bash

docker stop alg
docker rm alg
rm -f ~/.ssh/config.facont
rm -f ~/.ssh/facont_id_rsa*

