# -*- coding: utf-8 -*-

"""Fluid Asserts tracking module."""

# standard imports
import os
import hashlib
import sys
import platform

# 3rd party imports
from mixpanel import Mixpanel, MixpanelException

FA_EMAIL = 'engineering@fluidattacks.com'


def get_os_fingerprint() -> str:
    """Get fingerprint of running OS."""
    sha256 = hashlib.sha256()
    data = sys.platform + sys.version + platform.node()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()


def mp_track(func_to_track) -> bool:
    """Track a function."""
    success: bool = True
    if os.environ.get('FA_NOTRACK') != 'true':
        project_token = '4ddf91a8a2c9f309f6a967d3462a496c'
        user_id = get_os_fingerprint()
        mix_pan = Mixpanel(project_token)
        try:
            mix_pan.people_set(user_id, {'$email': FA_EMAIL})
            mix_pan.track(user_id, func_to_track, {
                'python_version': platform.python_version(),
                'platform': platform.system()})
        except MixpanelException:
            success = False
    return success
