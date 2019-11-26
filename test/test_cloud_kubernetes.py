# -*- coding: utf-8 -*-
"""Test module for fluidasserts.cloud.kubernetes."""
# standard imports
import os

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.kubernetes import deployments

KUBERNETES_APISERVER = os.environ['KUBERNETES_API_SERVER']
KUBERNETES_API_TOKEN = os.environ['KUBERNETES_API_TOKEN']


def test_runs_one_replica_per_deployment_open():
    """Search deployments runing only one replica."""
    assert deployments.runs_one_replica_per_deployment(
        host=KUBERNETES_APISERVER,
        api_key=KUBERNETES_API_TOKEN).is_open()
