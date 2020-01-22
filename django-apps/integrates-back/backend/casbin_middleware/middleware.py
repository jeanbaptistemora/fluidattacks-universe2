"""
Casbin Middleware.

Based on django-casbin
"""

# pylint: disable=no-self-use

import logging

import casbin

from django.core.exceptions import PermissionDenied

from backend import casbin_dynamodb_adapter


class CasbinMiddleware:
    """Casbin middleware."""

    def __init__(self, get_response):
        self.logger = logging.getLogger('casbin_middleware')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.get_response = get_response
        # Initialize the Casbin enforcer, executed only on once.
        adapter = casbin_dynamodb_adapter.Adapter()
        self.enforcer = casbin.Enforcer('integrates_authz_model.conf',
                                        adapter, True)

    def __call__(self, request):
        # Check the permission for each request.
        if not self.check_permission(request):
            # Not authorized, return HTTP 403 error.
            self.require_permission()

        # Permission passed, go to next module.
        response = self.get_response(request)
        return response

    def check_permission(self, request):
        # Customize it based on your authentication method.
        user = request.user.username
        if request.user.is_anonymous:
            user = 'anonymous'
        path = request.path
        method = request.method
        self.logger.info('User: %s, Path: %s, Method: %s', user, path, method)
        return self.enforcer.enforce(user, path, method)

    def require_permission(self,):
        raise PermissionDenied
