#!/bin/bash

docker stop integrates
docker rm integrates
rm -f ~/.ssh/config.facont.integrates
rm -f ~/.ssh/integrates_facont_id_rsa*
