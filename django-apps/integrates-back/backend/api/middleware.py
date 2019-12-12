from django.conf import settings
from graphql.backend.core import GraphQLCoreBackend
from graphql.language.ast import FragmentDefinition, FragmentSpread

from backend.exceptions import QueryDepthExceeded


def _get_depth(selection_set, fragments, depth_level=0):
    """
    Recursively calculates the query depth

    :param selection_set: requested attributes from the entity
    :param fragments: array of fragments definitions
    :param depth_level: current depth
    """
    max_depth = depth_level
    for field in selection_set.selections:
        if field.name.value not in settings.GRAPHQL['depth']['whitelist']:
            if isinstance(field, FragmentSpread):
                field = fragments[field.name.value]

            if field.selection_set:
                depth = _get_depth(
                    field.selection_set, fragments, depth_level + 1)
                if depth > max_depth:
                    max_depth = depth
    return max_depth


class ExecutorBackend(GraphQLCoreBackend):
    # pylint: disable=too-few-public-methods
    # Disabled because we only need to override a single method
    def document_from_string(self, schema, document_string):
        """
        Validates the query depth

        :param schema: GraphQL schema instance
        :param document_string: query string sent by the client
        """
        document = super(ExecutorBackend, self).document_from_string(
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
            if depth > settings.GRAPHQL['depth']['max'] and not settings.DEBUG:
                raise QueryDepthExceeded()
        return document
