#!/bin/bash

docker stop alg
docker rm alg
rm -f ~/.ssh/config.facont.alg
rm -f ~/.ssh/alg_facont_id_rsa*

