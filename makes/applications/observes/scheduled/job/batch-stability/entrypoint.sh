# shellcheck shell=bash
    alias stability="observes-bin-service-batch-stability"

    aws_login_prod 'observes' \
&&  stability default-queues "observes"
