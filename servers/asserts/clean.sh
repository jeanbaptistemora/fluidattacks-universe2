#!/bin/bash

docker stop asserts
docker rm asserts
rm -f ~/.ssh/config.facont.asserts
rm -f ~/.ssh/asserts_facont_id_rsa*
