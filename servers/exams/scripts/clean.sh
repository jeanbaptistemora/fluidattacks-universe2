#!/bin/bash

docker stop exams
docker rm exams
rm -f ~/.ssh/config.facont.exams
rm -f ~/.ssh/exams_facont_id_rsa*

