# -*- coding: utf-8 -*-

# pylint: disable=too-many-ancestors
# pylint: disable=unexpected-special-method-signature
# pylint: disable=super-init-not-called

"""This module provide tools to convert Cloudformation templates in graphs."""

# standar imports
import re
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict
from collections import UserDict
from collections import UserList
from contextlib import suppress
from copy import copy
from multiprocessing import cpu_count
from timeit import default_timer as timer
from typing import Tuple

# 3rd party imports
from pyparsing import Char
from pyparsing import nestedExpr
from pyparsing import Optional
from pyparsing import printables
from pyparsing import Suppress
from pyparsing import Word
from neo4j.exceptions import ClientError
import docker

# local imports
from fluidasserts.db.neo4j_connection import ConnectionString
from fluidasserts.db.neo4j_connection import driver_session
from fluidasserts.db.neo4j_connection import Session
from fluidasserts.helper.aws import _random_string
from fluidasserts.helper.aws import CLOUDFORMATION_EXTENSIONS
from fluidasserts.helper.aws import CloudFormationInvalidTemplateError
from fluidasserts.helper.aws import get_line
from fluidasserts.utils.generic import get_paths
from fluidasserts.helper.aws import load_cfn_template
from fluidasserts.helper.aws import retry_on_errors
from fluidasserts.utils.parsers.json import CustomDict
from fluidasserts.utils.parsers.json import CustomList


def create_alias(name: str, randoms=False) -> str:
    """Create an alias for Cipher statement.

    :param randoms: Add random chars to alias.
    """
    alias = name.replace('-', '_').lower().replace('::', '_').replace(
        ':', '_').replace('.', '_')
    if randoms:
        alias = f'{alias}_{_random_string(5)}'
    return alias


def _scan_sub_expresion(expresion) -> tuple:
    printables1 = copy(printables).replace('$', '')
    printables2 = copy(printables).replace('}', '')
    grammar = Suppress(Optional(Word(printables1))) + Suppress(
        Char('$')) + Optional(
            nestedExpr(opener='{', closer='}', content=Word(printables2)))
    result = []
    for reference in grammar.scanString(expresion):
        with suppress(IndexError):
            result.append(reference[0][0][0])
    return result


def _get_line(object_, key):
    line = None
    try:
        line = object_[f'{key}.line']
    except (KeyError, TypeError, AttributeError):
        try:
            line = get_line(object_[key])
        except KeyError:
            line = 0
        if line == 0:
            line = get_line(object_)
    return line if line != 0 else None


def is_primitive(item) -> bool:
    """Check if an object is of primitive type."""
    return not hasattr(item, '__dict__') and not isinstance(item, (list))


def _create_label(key: str) -> Tuple[str]:
    return (key.replace('-', '_').replace('::',
                                          ':').replace(' ', '_').replace(
                                              '.', '__'), key)


class List(UserList):
    """Custom list that passes items to neo4j nodes."""

    def __init__(self,
                 initlist,
                 father_id: int,
                 session: Session,
                 line,
                 **kwargs):
        """Convert input list to noe4j nodes.

        :param initlist: Input list.
        :param father_id: Id of parent node.
        :param session: Neo4j session.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.session = session
        statement = f"""
            MATCH (self)
            WHERE id(self) = {father_id}
            WITH self
            CREATE (self)-[:HAS]->(array:Array {{line: $line}})
            RETURN ID(array)
        """
        self.__id__ = self.session.run(statement, line=line).single().value()

        super().__init__(initlist)
        for index, item in enumerate(initlist):
            line = _get_line(initlist, index) or line
            self.__setitem__(index, item, line)

    def __sts_ref__(self, node_id: int = None):
        """Returns a reference to itself."""
        node_id = node_id or self.__id__
        return f"""
            MATCH (self)
            WHERE id(self) = {node_id}
            WITH self
        """

    def __setitem__(self, index, item, line):
        item_id = self.__create_node__(index, item, line)
        attrs = {'__references__': self.__references__,
                 '__path__': self.__path__}
        if is_primitive(item):
            self.data[index] = item
        elif isinstance(item, (list, CustomList)):
            self.data[index] = List(
                item, item_id, self.session, line=line, **attrs)
        elif isinstance(item, (dict, CustomDict)):
            self.data[index] = Dict(
                item, session=self.session, node_id=item_id, **attrs)

    def __setreferences__(self):
        """Create references between nodes."""
        for item in self.data:
            if isinstance(item, (Dict)):
                item.__setreferences__()
            elif isinstance(item, (List)):
                for value in item:
                    if hasattr(value, '__setreferences__'):
                        value.__setreferences__()

    def __create_node__(self, index, item, line):
        """Converts a list item to a neo4j node."""
        parameter = {'line': line}
        node_id = None
        node_properties = "{{line: $line, index: {index} {value}}}"
        if is_primitive(item):
            node_properties = node_properties.format(
                index=index, value=', value: $value')
            parameter.update({'value': item})
        else:
            node_properties = node_properties.format(index=index, value='')
        statement = f"""
            {self.__sts_ref__()}
            CREATE (self)-[:HAS]->(node:Item {node_properties})
            RETURN ID(node)
        """
        node_id = self.session.run(statement, **parameter).single().value()
        return node_id


class Dict(UserDict):
    """Custom dict that passes objects to neo4j nodes."""

    def __init__(self,
                 initial_dict,
                 path: str = None,
                 connection: ConnectionString = None,
                 session: Session = None,
                 node_id: int = None,
                 line: int = 0,
                 **kwargs):
        """Convert input dictionary to neo4j nodes.

        :param initial_dict: Initial dictionary.
        :param path: Path of cloudformation template.
        :param connection: Connection string to neo4j.
        :param session: Neo4j session.
        """
        # add additional properties
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.connection = connection
        self.__references__ = getattr(self, '__references__', dict())
        self.__line__ = line
        self.data = dict()

        # validate if exists properties
        if not session and not connection:
            raise Exception(
                'Must specify a begin session or a connection string')
        if not path and not node_id:
            raise Exception('Must specify a path or an id')

        # initialize a session if not exist or is the principal node
        if not session and connection:
            self.session = driver_session(self.connection)
        else:
            self.session = session
        # create template node
        if path:
            statement = """
            CREATE (template:CloudFormationTemplate {path: $path})
            RETURN ID(template)
            """
            self.__id__ = self.session.run(
                statement, path=path).single().value()
            self.__path__ = path
        else:
            self.__id__ = node_id

        for key, value in initial_dict.items():
            self.__line__ = _get_line(initial_dict, key) or self.__line__
            self.__setitem__(key, value, self.__line__)
        if connection:
            self.__setreferences__()
            self.session.close()

    def __create_reference__(self, dest: str = None):
        """Create a reference between itself and another resource.

        :param dest: Name of resource.
        """
        statement = "RETURN 1"
        if dest not in self.__references__ and re.fullmatch(
                r'AWS::(\w+|::)+', dest):
            statement = f"""{self.__sts_ref__()}
                            CREATE (self)-[:REFERENCE]->(
                                :{_create_label(dest)[0]})
                        """

            self.session.run(statement)
        elif dest in self.__references__:
            ref = self.__references__[dest]
            statement = f"""{self.__sts_ref__()}
                            MATCH (param)
                            WHERE id(param) = {ref}
                            WITH param, self
                            CREATE (self)-[:REFERENCE]->(param)
                        """

        self.session.run(statement)

    def __setreferences__(self):
        """Create references between nodes."""
        for key, item in self.data.items():
            if key == 'Ref':
                self.__create_reference__(item)
            elif key == 'Fn::Sub':
                self.__fn_sub__(item)
            elif key == 'Fn::FindInMap':
                self.__fn_findinmap__(item)
            elif key == 'Fn::GetAtt':
                ref = item.split('.')[0] if isinstance(
                    item, (str)) else item[0]
                self.__create_reference__(ref)
            elif key.startswith('Fn'):
                pass
            elif isinstance(item, (Dict)):
                item.__setreferences__()
            elif isinstance(item, (List)):
                item.__setreferences__()

    def __sts_ref__(self, node_id: int = None):
        """Returns a reference to itself."""
        node_id = node_id or self.__id__
        return f"""
            MATCH (self)
            WHERE id(self) = {node_id}
            WITH self
        """

    def __fn_sub__(self, item):
        if isinstance(item, (str)):
            references = _scan_sub_expresion(item)
            for ref in references:
                self.__create_reference__(ref)

    def __fn_findinmap__(self, item):
        if isinstance(item[0], (str)):
            label = _create_label(item[0])[0]
            statement = f"""
                MATCH (template:CloudFormationTemplate)-[:HAS]->(
                    :Mappings)-[:HAS]->(ref:{label})
                WHERE template.path = $path
                WITH ref
                {self.__sts_ref__()}, ref
                CREATE (self)-[:REFERENCE]->(ref)
            """
            self.session.run(statement, path=self.__path__)

    def __fn_getatt(self, item):
        ref = item.split('.')[0] if isinstance(item, (str)) else item[0]
        self.__create_reference__(ref)

    def __setitem__(self, key: str, item, line):
        if key.startswith('__'):
            return
        attrs = {
            '__node_name__': key,
            '__references__': self.__references__,
            '__path__': self.__path__
        }
        item_id = self.__create_node__(key, item, line)
        if is_primitive(item):
            if key == 'Type' and hasattr(self, '__node_name__'):
                self.__references__[self.__node_name__] = self.__id__
                if re.fullmatch(r'AWS::(\w+|::)+', item):
                    label = _create_label(item)[0]
                    statement = f"""
                        {self.__sts_ref__()}
                        SET self:{label}
                    """
                    self.session.run(statement)
            self.data[key] = item
        elif isinstance(item, (OrderedDict, CustomDict)):
            self.data[key] = Dict(
                item,
                session=self.session,
                node_id=item_id,
                line=self.__line__,
                **attrs)
        elif isinstance(item, (list, CustomList, List)):
            self.data[key] = List(item, item_id, self.session, line,
                                  **attrs)

    def __create_node__(self, key: str, item, line: int):
        """Converts a dictionary node to a neo4j node."""
        label, original = _create_label(key)
        parameter = {'line': line}
        node_id = None
        node_properties = "{{line: $line, name: $name {value}}}"
        relation = 'HAS'
        statement = f"{self.__sts_ref__()}\n"
        if is_primitive(item):
            node_properties = node_properties.format(value=', value: $value')
            parameter.update({'name': original, 'value': item})
        else:
            node_properties = node_properties.format(value='')
            parameter.update({'name': original})

        if key.startswith('Fn::') or key == 'Ref':
            relation = 'EXECUTE'
        statement += f"""
            CREATE (self)-[:{relation}]->(node:{label} {node_properties})
            WITH node
        """
        statement += "RETURN ID(node)"
        node_id = self.session.run(statement, **parameter).single().value()
        return node_id


class Loader:
    """Class to load cloudformation templates to neo4j."""

    def __init__(self,
                 create_db=True,
                 user: str = None,
                 passwd: str = None,
                 host: str = None,
                 port: int = None,
                 **kwargs):
        """Load cloudformation templates to Neo4j.

        If you do not want to connect to a database, a docker container will
        be created with an instance of the database. I was able to get the
        ``connection`` object for ses used in post-database queries.
        After using the database you must destroy it with the
        ``delete_database`` function.

        If you set the ``passwd`` parameter this will be the password that the
        database of the opposite will have, a random one will be created.

        :param connect_to_db: Connect to existant database.
        :param user: User to connect to the database.
        :param passwd: User password to connect to the database.
        :param host: Database host dir.
        :param port: Database port.
        """
        self.user = user or 'neo4j'
        self.password = passwd or _random_string(16)
        self.host = host
        self.port = port or 7687

        self.templates = []
        if create_db:
            self.create_db(retry=True, **kwargs)
        else:
            self.connection = ConnectionString(
                passwd=self.password,
                user=self.user,
                host=self.host,
                port=self.port,
                database=kwargs.get('database', None))

    def create_db(self, **kwargs):
        """Create a container with an instance of the database."""
        client = docker.from_env()
        environment = {
            'NEO4J_AUTH': f'{self.user}/{self.password}',
            'NEO4J_dbms_memory_heap_max__size': '4G',
            'NEO4J_dbms_memory_heap_initial__size': '2G',
            'NEO4J_dbms_memory_pagecache_size': '2G',
            'NEO4J_ACCEPT_LICENSE_AGREEMENT': 'yes',
        }
        container_name = kwargs.get(
            'container_name', None) or create_alias(f'asserts_neo4j', True)
        try:
            container_id = client.containers.run(
                'neo4j:enterprise',
                name=container_name,
                detach=True,
                environment=environment).attrs['Id']
            self.container_database = client.containers.get(container_id)
        except docker.errors.APIError as exc:
            if 'is already in use by container' in exc.explanation:
                self.container_database = client.containers.get(container_name)
                self.delete_database()
                self.create_db(**kwargs)
            else:
                raise exc

        self.host = self.container_database.attrs['NetworkSettings'][
            'Networks']['bridge']['IPAddress']
        self.connection = ConnectionString(
            user=self.user,
            passwd=self.password,
            host=self.host,
            port=self.port,
            database=kwargs.get('database', None))

    def delete_database(self):
        """Delete the database"""
        self.container_database.remove(force=True)

    @retry_on_errors
    def load_templates(self,
                       path: str,
                       exclude: list = None,
                       retry: bool = False):  # pylint: disable=unused-argument
        """Load all templates to the database.

        If you did not connect to a database use ``retry=True``.

        :param path: Path of cloudformation templates.
        :param exclude: Paths to exclude.
        """
        def load(_path_):
            with suppress(CloudFormationInvalidTemplateError):
                template = load_cfn_template(_path_)
                start_time = timer()
                success = True
                try:
                    Dict(template, path=_path_, connection=self.connection)
                except ClientError as exc:
                    error = str(exc)
                    success = False

                elapsed_time = timer() - start_time
                print(f'Loading: {_path_}')
                if success:
                    print((f'    [SUCCESS]    time: %.4f seconds') %
                          (elapsed_time))
                else:
                    print(f'    [ERROR] {error}')
        init_time = timer()
        with ThreadPoolExecutor(max_workers=cpu_count() * 3) as worker:
            worker.map(load, get_paths(
                path, exclude=exclude, endswith=CLOUDFORMATION_EXTENSIONS))
        end_time = timer() - init_time
        print(f'[SUCCESS]    Total: %.4f seconds' % (end_time))
