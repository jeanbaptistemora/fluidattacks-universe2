#!/bin/bash
aws s3 cp /tmp/FLUIDServes_Dynamic.pem s3://fluidpersistent/serves/
aws s3 cp /tmp/stackname.txt s3://fluidpersistent/serves/
