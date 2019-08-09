from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from social_core import exceptions as social_exceptions
from social_django.middleware import SocialAuthExceptionMiddleware
from graphql.backend.core import GraphQLCoreBackend
from graphql.language.ast import FragmentDefinition, FragmentSpread

from app.exceptions import ForbiddenField, QueryDepthExceeded


class SocialAuthException(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            exception_type = exception.__class__.__name__

            # An already logged in user attempted to access with a different account
            if exception_type == "AuthAlreadyAssociated":
                return HttpResponse('<script> \
                    localStorage.setItem("showAlreadyLoggedin","1"); \
                    if (location.origin.indexOf("://fluidattacks.com") === -1) { \
                        location = "/registration"; \
                    }else{ location = "/integrates/registration"; } </script>')

            # A user clicked return or stopped the page load after social auth
            elif exception_type in ["AuthCanceled", "AuthMissingParameter",
                                    "AuthStateMissing"]:
                return redirect("/index")
        else:
            return super(SocialAuthException, self).process_exception(request,
                                                                      exception)


def _get_depth(selection_set, fragments, depth_level=0):
    max_depth = depth_level
    for field in selection_set.selections:
        if isinstance(field, FragmentSpread):
            field = fragments[field.name.value]

        if field.selection_set:
            depth = _get_depth(field.selection_set, fragments, depth_level + 1)
            if depth > max_depth:
                max_depth = depth
    return max_depth


class GraphQLExecutorBackend(GraphQLCoreBackend):
    def document_from_string(self, schema, document_string):
        document = super(GraphQLExecutorBackend, self).document_from_string(
            schema, document_string)
        document_tree = document.document_ast
        query_tree = [definition
                      for definition in document_tree.definitions
                      if hasattr(definition, 'operation')
                      and definition.operation == 'query']
        fragments = {definition.name.value: definition
                     for definition in document_tree.definitions
                     if isinstance(definition, FragmentDefinition)}
        for field in query_tree:
            depth = _get_depth(field.selection_set, fragments)
            if depth > settings.GRAPHQL_MAX_QUERY_DEPTH and not settings.DEBUG:
                raise QueryDepthExceeded()
        return document


def graphql_blacklist_middleware(next_middleware, root, info, **kwargs):
    blacklisted_fields = ['__schema', '__type']
    if info.field_name.lower() in blacklisted_fields and not settings.DEBUG:
        raise ForbiddenField()
    return next_middleware(root, info, **kwargs)
