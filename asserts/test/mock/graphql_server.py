#!/usr/bin/env python3

"""Simple Flask/GraphQL server."""

from time import sleep
from flask import Flask
from flask_graphql import GraphQLView
from graphene import (Int, String, Boolean, Field, List,
                      Mutation, ObjectType, Schema)


#
# Database
#


DATA = {
    'Distro': {
        'Buzz',
        'Rex',
        'Bo',
        'Hamm',
        'Slink',
        'Potato',
        'Woody',
        'Sarge',
        'Etch',
        'Lenny',
        'Squeeze',
        'Wheezy',
        'Jessie',
        'Stretch',
        'Buster',
        'Bullseye',
        'Sid',
    },
    'User': {
        'Andrew': {
            'cpus': 4,
            'distros': {
                'Sid',
            },
        },
        'Kevin': {
            'cpus': 4,
            'distros': {
                'Buster',
                'Squeeze',
            },
        },
    }
}


#
# Middleware
#


def middleware_disable_introspection(next, root, info, **kwargs):
    """Middleware to disable introspection."""
    if info.field_name.lower() in ('__schema',
                                   '__field',
                                   '__type',
                                   '__typekind',
                                   '__inputvalue',
                                   '__enumvalue',
                                   '__directive',):
        raise Exception('Introspection is disabled')
    return next(root, info, **kwargs)


def middleware_slow_server(next, root, info, **kwargs):
    """Middleware to sleep between nodes simulating a loaded server."""
    sleep(1.0)
    return next(root, info, **kwargs)


#
# Queries
#


class Distro(ObjectType):
    """Distro class."""

    name = String()

    def __init__(self, name):
        """Constructor."""
        if name in DATA['Distro']:
            self.name = name

    def resolve_name(self, info):
        """Resolve name."""
        del info
        return self.name


class User(ObjectType):
    """User class."""

    name = String()
    cpus = Int()
    distros = List(Distro)

    def __init__(self, name):
        """Constructor."""
        if name in DATA['User']:
            self.name = name
            if 'cpus' in DATA['User'][name]:
                self.cpus = DATA['User'][name]['cpus']
            if 'distros' in DATA['User'][name]:
                self.distros = [
                    Distro(n) for n in DATA['User'][name]['distros']]

    def resolve_name(self, info):
        """Resolve name."""
        del info
        return self.name

    def resolve_cpus(self, info):
        """Resolve cpus."""
        del info
        return self.cpus

    def resolve_distros(self, info):
        """Resolve distros."""
        del info
        return self.distros


class Query(ObjectType):
    """Query class."""

    users = List(User)
    user = Field(User, name=String(required=True))

    distros = List(Distro)
    distro = Field(Distro, name=String(required=True))

    def resolve_user(self, info, name=None):
        """Resolve user."""
        del info
        return User(name)

    def resolve_users(self, info):
        """Resolve users."""
        del info
        return [User(name) for name in DATA['User']]

    def resolve_distro(self, info, name=None):
        """Resolve distro."""
        del info
        return Distro(name)

    def resolve_distros(self, info):
        """Resolve distros."""
        del info
        return [Distro(name) for name in DATA['Distro']]


#
#  Mutations
#


class EditUser(Mutation):
    """EditUser class."""

    class Arguments(object):
        """Arguments class."""

        name = String(required=True)
        cpus = Int(required=True)
        distros = List(String, required=True)

    success = Boolean()
    user = Field(User)

    def mutate(self, info, **kwargs):
        """Mutate function."""
        name = kwargs['name']
        cpus = kwargs['cpus']
        distros = kwargs['distros']

        if any(distro not in DATA['Distro'] for distro in distros):
            raise Exception('Invalid Distro')

        success = False
        if name in DATA['User'] and isinstance(distros, list):
            DATA['User'][name]['cpus'] = cpus
            DATA['User'][name]['distros'] = {distro for distro in distros}
            success = True

        return EditUser(success, User(name))


class Mutations(ObjectType):
    """Mutations class."""

    edit_user = EditUser.Field()


#
# Flask APP
#

APP = Flask('GraphQL Server')

APP.add_url_rule('/',
    endpoint='Home',
    view_func=lambda: 'Welcome to this Flask based GraphQL Server!')

APP.add_url_rule('/errors/invalid-json',
    endpoint='Errors',
    view_func=lambda: '{"Error": "I have an extra comma!",}')

APP.add_url_rule('/secure-graphql',
    view_func=GraphQLView.as_view('secure-graphql',
        schema=Schema(
            query=Query,
            mutation=Mutations,
            types=[]),
        graphiql=True,
        middleware=[
            middleware_disable_introspection,
        ]))

APP.add_url_rule('/insecure-graphql',
    view_func=GraphQLView.as_view('insecure-graphql',
        schema=Schema(
            query=Query,
            mutation=Mutations,
            types=[]),
        graphiql=True,
        middleware=[
        ]))

APP.add_url_rule('/lazy-graphql',
    view_func=GraphQLView.as_view('lazy-graphql',
        schema=Schema(
            query=Query,
            mutation=Mutations,
            types=[]),
        graphiql=True,
        middleware=[
            middleware_slow_server,
        ]))


def start():
    """Start this GraphQL Server."""
    try:
        APP.run(port=4001)
    except OSError:
        pass
