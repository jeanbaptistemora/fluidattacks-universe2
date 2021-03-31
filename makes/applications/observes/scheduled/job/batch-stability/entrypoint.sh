# shellcheck shell=bash

    aws_login_prod 'observes' \
&&  observes-bin-service-batch-stability
