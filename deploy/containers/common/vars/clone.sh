#!/bin/bash
git clone --depth 1 -b $CI_COMMIT_REF_NAME https://$FI_GITLAB_LOGIN:$FI_GITLAB_PASSWORD@gitlab.com/fluidsignal/integrates.git  /usr/src/app