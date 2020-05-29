# -*- coding: utf-8 -*-

# pylint: disable=too-many-lines
"""This module provide tools to convert Cloudformation templates in graphs."""

# standar imports
from collections import OrderedDict
from contextlib import suppress
from copy import copy
from timeit import default_timer as timer
from typing import List

# 3rd party imports
from pyparsing import Char
from pyparsing import nestedExpr
from pyparsing import Optional
from pyparsing import printables
from pyparsing import Suppress
from pyparsing import Word
import docker

# local imports
from fluidasserts.db.neo4j_connection import ConnectionString
from fluidasserts.db.neo4j_connection import database
from fluidasserts.db.neo4j_connection import runner
from fluidasserts.helper.aws import _random_string
from fluidasserts.helper.aws import CLOUDFORMATION_EXTENSIONS
from fluidasserts.helper.aws import CloudFormationInvalidTemplateError
from fluidasserts.helper.aws import get_line
from fluidasserts.utils.generic import get_paths
from fluidasserts.helper.aws import load_cfn_template
from fluidasserts.helper.aws import retry_on_errors
from fluidasserts.utils.parsers.json import CustomDict
from fluidasserts.utils.parsers.json import CustomList
from fluidasserts.utils.parsers.json import standardize_objects

INTRINSIC_FUNCS = [
    'Fn::Base64',
    'Fn::Cidr',
    'Fn::FindInMap',
    'Fn::GetAtt',
    'Fn::GetAZs',
    'Fn::ImportValue',
    'Fn::Join',
    'Fn::Select',
    'Fn::Split',
    'Fn::Sub',
    'Fn::Transform',
    'Ref',
    'Fn::And',
    'Fn::Equals',
    'Fn::If',
    'Fn::if',
    'Fn::Not',
    'Fn::Or'
]

CONDITIONAL_FUNCS = ['Fn::And', 'Fn::Equals',
                     'Fn::If', 'Fn::if', 'Fn::Not', 'Fn::Or']


def create_alias(name: str, randoms=False) -> str:
    """Create an alias for Cipher statement.

    :param randoms: Add random chars to alias.
    """
    alias = name.replace('-', '_').lower().replace('::', '_').replace(
        ':', '_').replace('.', '_')
    if randoms:
        alias = f'{alias}_{_random_string(5)}'
    return alias


def create_label(name: str) -> str:
    """Create an Label for Cipher statement."""
    return name.replace('-', '_').replace('::', ':')


def _fn_reference_logincal_id(logical_id: str) -> tuple:
    id_node = logical_id.replace('::', ':')
    alias_id = create_alias(id_node, True)
    return (alias_id, f"MERGE ({alias_id}:{id_node})\n")


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


class Batcher:  # noqa: H238
    """A class to convert a cloudformation template to graphs."""

    def __init__(self, template_path: str, connection=None, auto_commit=True):
        """Convert and load a clodformation template.

        Load the template and loop through all the nodes in the document
        to create a statement that loads the nodes to neo4j with their
        relationships.

        :param template_path: File path of CloudFormation template.
        :param session: Session that is already connected to the database.
        :param auto_commit: Load template automatically.
        """
        self.path = template_path
        self._load_template_data()
        self.statement_params = {}
        self.template['__node_name__'] = 'CloudFormationTemplate'
        self.template['__node_alias__'] = 'template'
        self.connection = connection
        self.transactions = []
        self.statements = []

        self.statements.append(self.create_template())
        self.statements.append(self.load_parameters())
        self.statements.append(self.load_mappings())
        self.statements.extend(self.load_conditions())
        self.statements.extend(self.load_resources())
        self.statements.append(self.load_outputs())

        if auto_commit:
            self.commit()

    def __call__(self, template_path: str, connection: ConnectionString):
        self.path = template_path
        self._load_template_data()
        self.statement_params = {}
        self.template['__node_name__'] = 'CloudFormationTemplate'
        self.template['__node_alias__'] = 'template'

        self.statements = []
        self.statements.append(self.create_template())
        self.statements.append(self.load_parameters())
        self.statements.append(self.load_mappings())
        self.statements.extend(self.load_conditions())
        self.statements.extend(self.load_resources())
        self.statements.append(self.load_outputs())
        self.commit()

    def commit(self):
        """Execute transaction."""
        with database(self.connection) as session:
            with runner(session) as transaction:
                for sts in self.statements:
                    transaction.run(sts, **self.statement_params)

    def _load_template_data(self):
        self.template = load_cfn_template(self.path)

    def _update_params(self, key, value):
        self.statement_params[key] = value

    def _clear_parmas(self):
        self.statement_params = dict()

    def create_template(self) -> str:
        """Create a node for the template with the basic information."""
        version = self.template.get('AWSTemplateFormatVersion', None)
        description = self.template.get('Description', None)
        alias = self.template['__node_alias__']
        node_name = self.template['__node_name__']

        statement = (f"CREATE ({alias}:{node_name} {{path: $path}})\n")
        statement += f"""
            CREATE ({alias})-[:HAS]->(:Attribute:AWSTemplateFormatVersion
                {{value: $version}})
            CREATE ({alias})-[:HAS]->(:Attribute:Description
             {{value: $description}})
             """

        self.statement_params.update({
            'path': self.path,
            'version': version,
            'description': description
        })
        return statement

    def _load_parameter_attributes(self, parameter: tuple) -> str:
        """Create a statement to create the attribute nodes of a parameter."""
        param_name, param_attrs = parameter
        alias_param = create_alias(param_name)
        statement = ""
        for attr_name, attr_value in param_attrs.items():
            if attr_name.startswith('__'):
                continue
            alias_attr_name = create_alias(attr_name)

            statement += f"""
                // create relationship between attribute and parameter
                CREATE (param_{alias_param})-[:HAS]->
                (:Attribute:{create_label(attr_name)}
                {{name: $param_{alias_param}_{alias_attr_name}_name,
                value: $param_{alias_param}_{alias_attr_name}_value,
                line: $param_{alias_param}_{alias_attr_name}_line}})
                """

            line = _get_line(param_attrs, attr_name)

            attr_value = standardize_objects(attr_value)
            self.statement_params.update({
                f'param_{alias_param}_{alias_attr_name}_name':
                attr_name,
                f'param_{alias_param}_{alias_attr_name}_value':
                attr_value,
                f'param_{alias_param}_{alias_attr_name}_line':
                line
            })
        return statement

    def _load_map_options(self, map_: tuple) -> str:
        """Create a statement to create the option nodes of a Mapping."""
        map_name, map_options = map_
        alias_map = create_alias(map_name)
        statement = ""

        for opt_name, opt_values in map_options.items():
            if opt_name.startswith('__'):
                continue
            alias_opt = create_alias(opt_name, True)

            statement += f"""
                        CREATE (map_{alias_map})-[:HAS]->
                        ({alias_map}_{alias_opt}_:MapOption:
                        {create_label(opt_name)} {{name:
                            $map_{alias_map}_{alias_opt}_name,
                            line: $map_{alias_map}_{alias_opt}_line}})
                        """

            line = _get_line(map_options, opt_name)
            self.statement_params.update({
                f'map_{alias_map}_{alias_opt}_line':
                line,
                f'map_{alias_map}_{alias_opt}_name':
                opt_name
            })

            opt_values = standardize_objects(opt_values)
            for var_name, var_value in opt_values.items():
                if var_name.startswith('__'):
                    continue
                line_var = _get_line(map_options[opt_name], var_name)

                statement += f"""
                    MERGE ({alias_map}_{alias_opt}_)-[:HAS]-
                    (:MapVar:{create_alias(var_name)}
                    {{name: ${alias_map}_{alias_opt}_{var_name}_name,
                     value: ${alias_map}_{alias_opt}_{var_name}_value,
                    line: ${alias_map}_{alias_opt}_{var_name}_line}})
                    """
                self.statement_params.update({
                    f'{alias_map}_{alias_opt}_{var_name}_name':
                    var_name,
                    f'{alias_map}_{alias_opt}_{var_name}_value':
                    var_value,
                    f'{alias_map}_{alias_opt}_{var_name}_line':
                    line_var
                })

        return statement

    def load_parameters(self) -> str:
        """Execute a statement that creates the nodes for the template params.

        :param trans: Transaction to execute the statement.
        """
        if 'Parameters' not in self.template.keys():
            return 'RETURN 1'
        alias_parameters = self.template['Parameters'][
            '__node_alias__'] = "params"

        node_template_name = self.template['__node_name__']
        statement = f"""
                    MATCH (template:{node_template_name})
                    WHERE template.path = "{self.path}"
                    CREATE (template)-[:HAS]->({alias_parameters}:Parameters
                    {{line: ${alias_parameters}_line}})
                    """
        self.statement_params[f'{alias_parameters}_line'] = get_line(
            self.template['Parameters'])

        for param_name, param_attrs in self.template['Parameters'].items():
            if param_name.startswith('__'):
                continue
            alias_param = create_alias(param_name)
            # create the node for the parameter
            param_statement = f"""
                CREATE ({alias_parameters})-[:HAS]->
                (param_{alias_param}:Reference:Parameter:
                {create_label(param_name)}
                // set attributes of nod
                 {{logicalName: $param_{alias_param},
                 line: ${alias_param}_line}})
                """
            self.statement_params.update({
                f'param_{alias_param}':
                param_name,
                f'{alias_param}_line':
                get_line(self.template['Parameters'][param_name])
            })
            # add parameter attributes
            param_statement += self._load_parameter_attributes((param_name,
                                                                param_attrs))
            statement += param_statement

        return statement

    def load_mappings(self) -> str:
        """Execute a statement that creates nodes for the template Mappings.

        :param trans: Transaction to execute the statement.
        """
        if 'Mappings' not in self.template.keys():
            return 'RETURN 1'
        alias_mappings = self.template['Mappings'][
            '__node_alias__'] = "mappings"
        node_template_name = self.template['__node_name__']

        statement = f"""
                    MATCH (template:{node_template_name})
                    WHERE template.path = "{self.path}"
                    CREATE (template)-[:HAS ]->
                    ({alias_mappings}:Mappings
                    {{line: ${alias_mappings}_line}})
                    """
        self.statement_params[f'{alias_mappings}_line'] = get_line(
            self.template['Mappings'])

        for map_name, map_options in self.template['Mappings'].items():
            if map_name.startswith('__'):
                continue
            line = _get_line(self.template['Mappings'], map_name)
            if map_name.startswith('Fn::'):
                contexts = {alias_mappings}
                statement += self.load_intrinsic_func(
                    alias_mappings, map_name, map_options, contexts, line)
                continue
            alias_map = create_alias(map_name)
            map_statement = f"""
                CREATE ({alias_mappings})-[:HAS]->
                (map_{alias_map}:Mapping:{create_label(map_name)}
                {{name: $map_name_{alias_map}, line: ${alias_map}_line}})
                """

            self.statement_params.update({
                f'map_name_{alias_map}': map_name,
                f'{alias_map}_line': line
            })

            map_statement += self._load_map_options((map_name, map_options))

            statement += map_statement
        return statement

    def load_conditions(self) -> List[str]:
        """Execute a statement that creates nodes for the template Conditions.

        :param trans: Transaction to execute the statement.
        """
        if 'Conditions' not in self.template.keys():
            return ['RETURN 1']

        statements = []
        alias_conditions = self.template['Conditions'][
            '__node_alias__'] = "conditions_node"
        node_template_name = self.template['__node_name__']
        # create relationship between templeate and node conditions
        statement = f"""
                MATCH (template:{node_template_name})
                WHERE template.path = "{self.path}"
                CREATE (template)-[:HAS]->({alias_conditions}:Conditions
                {{line: ${alias_conditions}_line}})
                """

        self.statement_params[f'{alias_conditions}_line'] = get_line(
            self.template['Conditions'])
        # Create create relationship between contition nodes and each condition
        for con_name, condition in self.template['Conditions'].items():
            if con_name.startswith('__'):
                continue
            if con_name.startswith('Fn::'):
                contexts = {alias_conditions}
                statement += self.load_intrinsic_func(
                    alias_conditions, con_name, condition, contexts)
                continue
            alias_con = create_alias(f"con_{con_name}")
            statement += f"""
                    CREATE ({alias_conditions})-[:HAS]->
                    ({alias_con}:Condition:{create_label(con_name)}
                    {{name: $con_name_{alias_con},
                    line: ${alias_con}_line}})
                    """
            self.statement_params.update({
                f'con_name_{alias_con}':
                con_name,
                f'{alias_con}_line':
                _get_line(self.template['Conditions'], con_name)
            })

        statements.append(statement)

        # create relationship between the conditions and the functions that
        # each one executes
        for con_name, condition in self.template['Conditions'].items():
            if con_name.startswith('__') or con_name.startswith('Fn::'):
                continue
            alias_condition = create_alias(f"con_{con_name}")
            # create reference to condition
            statement_condition = f"""
                MATCH (template:{node_template_name})-[*]->
                ({alias_condition}:Condition)
                WHERE template.path = '{self.path}' AND
                {alias_condition}.name = ${alias_condition}_value
                """
            self.statement_params[f'{alias_condition}_value'] = con_name
            # create relationship between the condition and the function it
            #  executes
            line = _get_line(self.template['Conditions'], con_name)
            statement_condition += self._load_condition_funcs(
                (alias_condition, condition), {alias_condition}, line)
            statements.append(statement)
        return statements

    def load_resources(self) -> List[str]:
        """Execute a statement that creates nodes for the template Resources.

        :param trans: Transaction to execute the statement.
        """
        alias_resours = "resources_node"
        node_template_name = self.template['__node_name__']
        # create relationship between templeate and node conditions
        sts = []
        statement = f"""
            MATCH (template:{node_template_name})
            WHERE template.path = "{self.path}"
            MERGE (template)-[:HAS]->({alias_resours}:Resources
            {{line: ${alias_resours}_line}})
                """
        self.statement_params[f'{alias_resours}_line'] = get_line(
            self.template['Resources'])

        self.statements.append(statement)
        for resource_name in self.template['Resources'].keys():
            loaded = False
            with suppress(KeyError, TypeError):
                loaded = self.template['Resources'][resource_name][
                    '__loaded__'] or loaded
            if resource_name.startswith('__') or loaded:
                continue

            if resource_name.startswith('Fn::'):
                contexts = {alias_resours}
                statement = statement + self.load_intrinsic_func(
                    alias_resours, resource_name,
                    self.template['Resources'][resource_name], contexts)
                sts.append(statement)
            else:
                sts.extend(self._load_resource(resource_name))
        return sts

    def load_outputs(self) -> str:
        """Execute a statement that creates the nodes for the template Outputs.

        :param trans: Transaction to execute the statement.
        """
        if 'Outputs' not in self.template.keys():
            return 'RETURN 1'
        alias_outputs = self.template['Outputs'][
            '__node_alias__'] = "resources_node"
        node_template_name = self.template['__node_name__']
        statement = f"""
                MATCH (template:{node_template_name})
                WHERE template.path = $template_path
                CREATE (template)-[:HAS]->({alias_outputs}:Outputs
                 {{line: ${alias_outputs}_line}})
                     """
        self.statement_params.update({
            f'{alias_outputs}_line':
            get_line(self.template['Outputs']),
            'template_path':
            self.path
        })

        contexts = {alias_outputs}
        for out_name, out_value in self.template['Outputs'].items():
            if out_name.startswith('__'):
                continue
            if out_name.startswith('Fn::'):
                statement += self.load_intrinsic_func(alias_outputs, out_name,
                                                      out_value, contexts)
                continue
            alias_out = create_alias(out_name, True)
            statement += f"""
                CREATE ({alias_outputs})-[:HAS]->(
                    {alias_out}:Output:{create_label(out_name)}
                {{Description: $out_desc{alias_out},
                 line: ${alias_out}_line}})\n
                          """
            contexts.add(alias_out)
            line = _get_line(self.template['Outputs'], out_name)
            self.statement_params.update({
                f'out_name{alias_out}':
                out_name,
                f'{alias_out}_line':
                line,
                f'out_desc{alias_out}':
                out_value.get('Description', 'nothing')
            })

            alias_value = create_alias(f'{alias_out}_value')
            statement += f"""
                CREATE ({alias_out})-[:HAS]->({alias_value}:Attribute:Value)
                    """

            contexts.add(alias_value)
            if isinstance(out_value['Value'], (int, str, bool)):
                statement += (
                    f'SET {alias_value}.value = ${alias_value}_value\n')
                self.statement_params[f'{alias_value}_value'] = out_value[
                    'Value']
            else:
                func_name = list(out_value['Value'].keys())[0]
                line = _get_line(out_value['Value'], func_name)
                statement += self.load_intrinsic_func(
                    alias_value, func_name, out_value['Value'][func_name],
                    contexts, line)
            if 'Export' in out_value:
                alias_export = create_alias(f'{alias_out}_export')
                contexts.add(alias_export)
                statement += f"""
                    CREATE ({alias_out})-[:HAS]->(
                        {alias_export}:Attribute:Export)
                        """
                if isinstance(out_value['Export'], (int, str, bool)):
                    statement += (
                        f'SET {alias_export}.value = ${alias_export}_value\n')
                    self.statement_params[f'{alias_export}_value'] = out_value[
                        'Export']
                else:
                    line = _get_line(out_value, 'Export')
                    statement += self._load_resource_property(
                        (alias_export, out_value['Export']), contexts, line)
        return statement

    def _load_resource(self, resource_name) -> List[str]:
        alias_resources = "resources_node"
        alias_template = self.template['__node_alias__']
        node_template_name = self.template['__node_name__']
        resource = self.template['Resources'][resource_name]
        resource_node = resource['Type'].replace('::', ':')
        res_alias = create_alias(resource_name, True)

        sts = []
        statement = f"""
            MATCH ({alias_template}:{node_template_name})-[:HAS]->
            ({alias_resources}:Resources)
            WHERE {alias_template}.path = "{self.path}"
            CREATE ({alias_resources})-[:HAS]->({res_alias}:Reference:
                {resource_node}:{resource_name} {{
            Name:${res_alias}_name, logicalName:${res_alias}_name,
             line: ${res_alias}_line}})-[:HAS]->({res_alias}props:Properties
                {{line: ${res_alias}props_line}})
            """
        sts.append(statement)
        self.statement_params.update({f'{res_alias}_name': resource_name})
        line = _get_line(self.template['Resources'], resource_name)
        self.statement_params[f'{res_alias}_line'] = line
        line = _get_line(resource, 'Properties') or line
        self.statement_params[f'{res_alias}props_line'] = line
        for prop_name, prop_value in resource.get('Properties',
                                                  dict()).items():
            if prop_name.startswith('__'):
                continue
            prop_alias = create_alias(f'{res_alias}_{prop_name}', True)
            line = _get_line(resource['Properties'], prop_name) or line
            contexts = {prop_alias}

            statement = f"""
                MATCH (template:{node_template_name})-[*]->
                (resource: Reference)-[*]->(properties:Properties)
                WHERE template.path = '{self.path}' AND
                resource.logicalName = ${res_alias}_name
                CREATE (properties)-[:HAS]->({prop_alias}:{prop_name} {{
                name: ${prop_alias}_name, line: ${prop_alias}_line}})
                """
            self.statement_params[f'{prop_alias}_name'] = prop_name
            self.statement_params[f'{prop_alias}_line'] = line
            statement += self._load_resource_property((prop_alias, prop_value),
                                                      contexts, line)
            sts.append(statement)
        self.template['Resources'][resource_name]['__loaded__'] = True
        return sts

    def _load_resource_property(self,
                                property_: tuple,
                                contexts: set,
                                line='unknown') -> str:
        prop_alias, prop_value = property_
        statement = ""
        if isinstance(prop_value, (str, int, bool)):
            statement += (f"SET {prop_alias}.value = ${prop_alias}_value\n")
            self.statement_params[f'{prop_alias}_value'] = prop_value
        elif isinstance(prop_value, (OrderedDict, CustomDict)) and len(
                prop_value) > 0:
            func_name = list(prop_value.keys())[0]
            if func_name in INTRINSIC_FUNCS:
                return self.load_intrinsic_func(
                    prop_alias, func_name, prop_value[func_name], contexts,
                    _get_line(prop_value, func_name) or line)
            for key, value in prop_value.items():
                if key.startswith('__'):
                    continue
                attr_alias = create_alias(f'{prop_alias}_{key}', True)
                contexts.add(attr_alias)
                line = _get_line(prop_value, key) or line
                property_name = key.replace('-', '__')
                statement += f"""
                    CREATE ({prop_alias})-[:HAS]->(
                        {attr_alias}:PropertyAttribute:
                    {create_label(property_name)} {{line: ${attr_alias}_line}})
                    """
                self.statement_params[f'{attr_alias}_line'] = line
                statement += self._load_resource_property((attr_alias, value),
                                                          contexts, line)
        elif isinstance(prop_value, (list, CustomList)):
            statement += f"SET {prop_alias} :Array\n"
            for idx, value in enumerate(prop_value):
                alias_item = create_alias(f'{prop_alias}_{idx}', True)
                line = _get_line(prop_value, idx) or line
                statement += f"""
                    CREATE ({prop_alias})-[:HAS]->({alias_item}:Item
                        {{index: {idx}, line: ${alias_item}_line}})
                    """
                self.statement_params[f'{alias_item}_line'] = line
                contexts.add(alias_item)
                statement += self._load_resource_property((alias_item, value),
                                                          contexts, line)
        return statement

    def _load_condition_funcs(self, func: tuple, context: set, line=0) -> str:
        """Create a statement to load a function.

        Context lets inherit contexts from top nodes to create relationships.
        :param func: Function to load.
        :param context: Context to execute statements.
        """
        alias_f, func_exc = func
        fn_name = list(func_exc.keys())[0]

        line = _get_line(func_exc, fn_name) or line
        if fn_name not in INTRINSIC_FUNCS:
            raise Exception(f'{fn_name} function is not supported.')

        return self.load_intrinsic_func(alias_f, fn_name, func_exc[fn_name],
                                        context, line)

    def load_intrinsic_func(self,
                            resource_alias: str,
                            func_name,
                            attrs,
                            contexts: set = None,
                            line='unknown',
                            **kwargs) -> str:
        """Create a statement to load clodformation intrinsic functions.

        :param resource_alias: Resource that is related to the function.
        :param func_name: Name of intrinsic function.
        :param attrs: Attributes of function.
        """
        contexts = contexts or set([])
        contexts_str = ', '.join(contexts)
        statement = f"WITH {contexts_str}\n"
        functions = {
            'Fn::Base64': self._fn_base64,
            'Ref': self._fn_reference,
            'Fn::GetAtt': self._fn_getatt,
            'Fn::Cidr': self._fn_cidr,
            'Fn::GetAZs': self._fn_get_azs,
            'Fn::FindInMap': self._fn_find_in_map,
            'Fn::Sub': self._fn_sub,
            'Fn::Join': self._fn_join,
            'Fn::Split': self._fn_split,
            'Fn::Select': self._fn_select,
            'Fn::Transform': self._fn_transform,
            'Fn::ImportValue': self._fn_importvalue,
        }

        if functions.get(func_name, None):
            statement += functions.get(func_name)(resource_alias, attrs,
                                                  contexts, line, **kwargs)
        elif func_name in CONDITIONAL_FUNCS:
            statement += self._fn_conditional(func_name, resource_alias, attrs,
                                              contexts, line, **kwargs)

        return statement

    def _fn_base64(self,
                   resource_id,
                   attrs,
                   contexts: set = None,
                   line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::Base64."""
        contexts = contexts or set({})
        alias_fn = create_alias("fn_base_base64", True)
        alias_value = create_alias(f'{alias_fn}_value')

        statement = f"""
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:Fn:Base64
                {{line: ${alias_fn}_line}})-[:HAS]->
            ({alias_value}:Value:ValueToEncode {{line: ${alias_fn}_line}})
                """
        self.statement_params[f'{alias_fn}_line'] = line
        contexts.update([alias_fn, alias_value])

        if isinstance(attrs, (str, int, bool)):
            statement += f"SET {alias_value}.value = ${alias_value}_value\n"
            self.statement_params[f'{alias_value}_value'] = attrs
        elif isinstance(attrs, (OrderedDict, CustomDict)):
            for key, _ in attrs.items():
                if key.startswith('__'):
                    continue
                line = _get_line(attrs, key) or line
                statement += self.load_intrinsic_func(
                    alias_value, key, attrs[key], contexts, line)

        return statement

    def _fn_reference(self,
                      resource_id: str,
                      logical_name: str,
                      contexts: set = None,
                      line='unknown',
                      direct_reference=False) -> str:
        """Loaf intrinsic function Ref."""
        node_template_name = self.template['__node_name__']
        contexts = contexts or set([])
        ref_alias = create_alias(f'ref_{resource_id}_{logical_name}', True)
        statement = ""
        if logical_name in self.template['Resources'].keys(
        ) and '__loaded__' not in self.template['Resources'][logical_name]:
            self.statements.extend(self._load_resource(logical_name))

        self.statement_params[f'{ref_alias}_line'] = line
        if not direct_reference:
            contexts.update([ref_alias])
            contexts_str = ', '.join(contexts)
            statement += f"""
                CREATE ({resource_id})-[:EXECUTE_FN]->({ref_alias}:Ref
                {{logicalName:${ref_alias}_log_name, line:${ref_alias}_line}})
                WITH {contexts_str}
                """
        else:
            ref_alias = resource_id
            contexts.add(ref_alias)

        param_alias = create_alias(f'ref_{resource_id}_{logical_name}')
        if not logical_name.startswith('AWS::'):
            statement += f"""
                MATCH (template:{node_template_name})-[*]->
                ({param_alias}: Reference)
                WHERE template.path = '{self.path}' AND
                {param_alias}.logicalName = ${param_alias}_name
                CREATE ({ref_alias})-[:REFERENCE_TO]->({param_alias})
                """
            contexts.update([param_alias])
        else:
            log_id, log_sts = _fn_reference_logincal_id(logical_name)
            statement += f"""
                {log_sts} CREATE ({ref_alias})-[:REFERENCE_TO]->({log_id})
                """
        self.statement_params.update({
            f'{param_alias}_line': line,
            f'{ref_alias}_log_name': logical_name,
            f'{param_alias}_name': logical_name
        })

        return statement

    def _fn_getatt(self,
                   resource_id: str,
                   attrs,
                   contexts: set = None,
                   line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::GettAtt."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_getatt", True)
        contexts.add(alias_fn)
        contexts_str = ', '.join(contexts)

        statement = f"""
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:Fn:GetAtt
                {{line: ${alias_fn}_line}})
            WITH {contexts_str}
            """
        self.statement_params[f'{alias_fn}_line'] = line

        # load logical name of resource
        statement += f"""
            CREATE ({alias_fn})-[:HAS]->(
                {alias_fn}log:Value:LogicalNameOfResource {{
                    line: ${alias_fn}_line}})
            CREATE ({alias_fn})-[:HAS]->({alias_fn}att:Value:AttributeName {{
                line: ${alias_fn}_line}})
                """
        contexts.update([f'{alias_fn}log', f'{alias_fn}att'])
        if isinstance(attrs, str):
            contexts_str = ', '.join(contexts)
            resource_attr = attrs.split('.')[0]
            resource = resource_attr[0]
            attr = resource_attr[1] if len(resource_attr) > 1 else 'nothing'
            statement += f"""
                SET {alias_fn}log.value = ${alias_fn}_log
                SET {alias_fn}att.value = ${alias_fn}_att
                WITH {contexts_str}
                    """
            self.statement_params.update({
                f'{alias_fn}_log': resource,
                f'{alias_fn}_att': attr
            })

            statement += self._fn_reference(
                alias_fn, resource, contexts, line, direct_reference=True)
        else:
            contexts_str = ', '.join(contexts)
            statement += f"""
                SET {alias_fn}log.value = ${alias_fn}_log
                WITH {contexts_str}
                """
            self.statement_params[f'{alias_fn}_log'] = attrs[0]
            statement += self._fn_reference(
                alias_fn, attrs[0], contexts, line, direct_reference=True)
            if not isinstance(attrs[1], (OrderedDict, CustomDict)):
                statement += f"SET {alias_fn}att.value = ${alias_fn}_att\n"
                self.statement_params[f'{alias_fn}_att'] = attrs[1]
            else:
                func_name = list(attrs[1].keys())[0]
                line = _get_line(attrs[1], func_name) or line
                statement += self.load_intrinsic_func(
                    f'{alias_fn}att', func_name, attrs[1][func_name], contexts,
                    line)
        return statement

    def _fn_cidr(self,
                 resource_id: str,
                 attrs,
                 contexts: set = None,
                 line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::Cidr."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_getatt", True)

        statement = f"""
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:Fn:Cidr
                {{line: ${alias_fn}_line}})
                """
        contexts.add(alias_fn)

        # load ipBlock
        statement += f"""
            CREATE ({alias_fn})-[:HAS]->({alias_fn}ipblock:Value:IpBlock {{
                line: ${alias_fn}_line}})
            """
        contexts.add(f'{alias_fn}ipblock')
        if isinstance(attrs[0], str):
            statement += f"SET {alias_fn}_ipblock.value = ${alias_fn}ipblock\n"
            self.statement_params[f'{alias_fn}ipblock'] = attrs[0]
        else:
            func_name = list(attrs[0].keys())[0]
            statement += self.load_intrinsic_func(
                f'{alias_fn}ipblock', func_name, attrs[0][func_name], contexts,
                _get_line(attrs[0], func_name) or line)

        # load count
        statement += f"""
            CREATE ({alias_fn})-[:HAS]->({alias_fn}count:Value:Count {{
                line: ${alias_fn}_line}})
            """
        contexts.add(f'{alias_fn}count')
        if isinstance(attrs[1], (str, int)):
            statement += f"SET {alias_fn}count.value = ${alias_fn}count\n"
            self.statement_params[f'{alias_fn}count'] = attrs[1]
        else:
            func_name = list(attrs[1].keys())[0]
            statement += self.load_intrinsic_func(
                f'{alias_fn}count', func_name, attrs[1][func_name], contexts,
                _get_line(attrs, 1) or line)

        # load cidrBits
        statement += f"""
                CREATE ({alias_fn})-[:HAS]->({alias_fn}cidr:Value:CidrBits {{
                    line: ${alias_fn}_line}})
                """
        contexts.add(f'{alias_fn}cidr')
        if isinstance(attrs[2], (str, int)):
            statement += f"SET {alias_fn}cidr.value = ${alias_fn}cidrbits\n"
            self.statement_params[f'{alias_fn}cidrbits'] = attrs[2]
        else:
            func_name = list(attrs[2].keys())[0]
            statement += self.load_intrinsic_func(
                f'{alias_fn}cidr', func_name, attrs[2][func_name], contexts,
                _get_line(attrs[2], func_name) or line)

        self.statement_params[f'{alias_fn}_line'] = line

        return statement

    def _fn_find_in_map(self,
                        resource_id: str,
                        attrs,
                        contexts: set = None,
                        line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::FindInMap."""
        node_template_name = self.template['__node_name__']
        contexts = contexts or set([])
        alias_fn = create_alias("fn_findinmap", True)
        alias_mapping = create_alias(f'{attrs[0]}_mapping', True)
        contexts.add(alias_mapping)
        contexts_str = ', '.join(contexts)

        statement = f"""
            MATCH (template:{node_template_name})-[*]->
            ({alias_mapping}:Mapping)
            WHERE template.path = '{self.path}' AND
            {alias_mapping}.name = ${alias_mapping}_name
            WITH {contexts_str}
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:Fn:FindInMap
                {{line: ${alias_fn}_line}})-[:REFERENCE_TO]->({alias_mapping})
            """
        contexts.add(alias_fn)
        self.statement_params.update({
            f'{alias_mapping}_name': attrs[0],
            f'{alias_fn}_line': line,
            f'{alias_fn}_mapname': attrs[0]
        })

        # load mapname
        statement += f"""
            CREATE ({alias_fn})-[:HAS]->({alias_fn}map:Value:MapName
                {{value: ${alias_fn}_mapname, line: ${alias_fn}_line}})
            """
        contexts.add(f'{alias_fn}map')

        # load toplevel key
        statement += f"""
            CREATE ({alias_fn})-[:HAS]->({alias_fn}top:Value:TopLevelKey {{
                line: ${alias_fn}_line}})
            """
        contexts.add(f'{alias_fn}top')
        if isinstance(attrs[1], (str)):
            statement += f"SET {alias_fn}top.value = ${alias_fn}_top\n"
            self.statement_params[f'{alias_fn}_top'] = attrs[1]
        else:
            func_name = list(attrs[1].keys())[0]
            statement += self.load_intrinsic_func(
                f'{alias_fn}top', func_name, attrs[1][func_name], contexts,
                _get_line(attrs[1], func_name) or line)

        # load second level key
        statement += f"""
            CREATE ({alias_fn})-[:HAS]->(
                {alias_fn}sec:Value:SecondLevelKey {{line: ${alias_fn}_line}})
                """
        contexts.add(f'{alias_fn}sec')
        if isinstance(attrs[2], (str)):
            statement += f"SET {alias_fn}sec.value = ${alias_fn}_sec\n"
            self.statement_params[f'{alias_fn}_sec'] = attrs[2]
        else:
            func_name = list(attrs[2].keys())[0]
            statement += self.load_intrinsic_func(
                f'{alias_fn}sec', func_name, attrs[2][func_name], contexts,
                _get_line(attrs[2], func_name) or line)

        return statement

    def _fn_get_azs(self,
                    resource_id: str,
                    attrs,
                    contexts: set = None,
                    line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::GetAZs."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_getazs", True)
        statement = f"""
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:Fn:GetZAs {{
                line: ${alias_fn}_line}})-[:HAS]->({alias_fn}reg:Value:Region
            {{line: ${alias_fn}_line}})
            """
        self.statement_params[f'{alias_fn}_line'] = line
        contexts.update([alias_fn, f'{alias_fn}reg'])
        if isinstance(attrs, str):
            statement += f"SET {alias_fn}reg.region = ${alias_fn}_region\n"
            self.statement_params[f'{alias_fn}_region'] = attrs
        else:
            func_name = list(attrs.keys())[0]
            line = _get_line(attrs, func_name) or line
            statement += self.load_intrinsic_func(
                f'{alias_fn}reg', func_name, attrs[func_name], contexts, line)

        return statement

    def _fn_sub(self,
                resource_id: str,
                attrs,
                contexts: set = None,
                line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::Sub."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_sub", True)

        statement = f"""
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:Fn:Sub {{
                line: ${alias_fn}_line}})-[:HAS]->(:Value:String {{
                    value: ${alias_fn}_string, line: ${alias_fn}_line}})
            """
        self.statement_params[f'{alias_fn}_line'] = line
        contexts.add(alias_fn)
        if isinstance(attrs, str):
            self.statement_params[f'{alias_fn}_string'] = attrs
            references = _scan_sub_expresion(attrs)
            for ref in references:
                contexts_str = ', '.join(contexts)
                statement += f"WITH {contexts_str}\n"
                if '.' in ref:
                    resource = ref.split('.')[0]
                    statement += self._fn_reference(
                        alias_fn, resource, direct_reference=True)
                else:
                    ref_sts = self._fn_reference(
                        alias_fn, ref, contexts, direct_reference=True)
                    statement += ref_sts
        else:
            self.statement_params[f'{alias_fn}_string'] = attrs[0]
            references = _scan_sub_expresion(attrs[0])
            for key, value in attrs[1].items():
                if key.startswith('__'):
                    continue
                alias_var = create_alias(f'{alias_fn}_{key}', True)
                statement += f"""
                    CREATE ({alias_fn})-[:HAS]->(
                        {alias_var}:Value:Var:{create_label(key)} {{
                            line: ${alias_fn}_line}})
                        """
                contexts.add(alias_var)
                if isinstance(value, (bool, str, int)):
                    statement += (
                        f"SET {alias_var}.value = ${alias_fn}_{key}\n")
                    self.statement_params[f'{alias_fn}_{key}'] = value
                else:
                    func_name = list(attrs[1][key].keys())[0]
                    line = _get_line(attrs[1][key], func_name) or line
                    statement += self.load_intrinsic_func(
                        alias_var, func_name, attrs[1][key][func_name],
                        contexts, line)

        return statement

    def _fn_join(self,
                 resource_id: str,
                 attrs,
                 contexts: set = None,
                 line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::Join."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_join", True)

        statement = f"""
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:Fn:Join {{
                line: ${alias_fn}_line}})-[:HAS]->(:Value:Delimiter {{
                    value:${alias_fn}_delimiter, line:${alias_fn}_line }})
            """
        self.statement_params.update({
            f'{alias_fn}_delimiter': attrs[0],
            f'{alias_fn}_line': line
        })

        statement += f"""
            CREATE ({alias_fn})-[:HAS]->({alias_fn}list:Value:List {{
                line: ${alias_fn}_line}})
                      """
        contexts.update([alias_fn, f'{alias_fn}list'])
        for idx, value in enumerate(attrs[1]):
            statement += f"""
                CREATE ({alias_fn}list)-[:HAS]->({alias_fn}list{idx}:Value:Item
                    {{index: {idx}, line:${alias_fn}_line}})
                """
            contexts.add(f'{alias_fn}list{idx}')
            if isinstance(value, (str, bool, int)):
                statement += (
                    f"SET {alias_fn}list{idx}.value = ${alias_fn}_val{idx+1}\n"
                )
                self.statement_params[f'{alias_fn}_val{idx+1}'] = value
            else:
                func_name = list(value.keys())[0]
                line = _get_line(attrs[1][idx], func_name) or line
                statement += self.load_intrinsic_func(
                    f'{alias_fn}list{idx}', func_name, value[func_name],
                    contexts, line)

        return statement

    def _fn_split(self,
                  resource_id: str,
                  attrs,
                  contexts: set = None,
                  line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::Split."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_split", True)
        contexts.add(alias_fn)

        statement = f"""
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:Fn:Split {{
                line: ${alias_fn}_line}})-[:HAS]->(:Value:Delimiter {{
                    value: ${alias_fn}_delimiter, line:${alias_fn}_line}})
            """
        self.statement_params.update({
            f'{alias_fn}_delimiter': attrs[0],
            f'{alias_fn}_line': line
        })

        statement += f"""
            CREATE ({alias_fn})-[:HAS]->({alias_fn}str:Value:SourceString {{
                line: ${alias_fn}_line}})\
            """
        if isinstance(attrs[1], (str, bool, int)):
            statement += (f"SET {alias_fn}str.value = ${alias_fn}_val\n")
            self.statement_params[f'{alias_fn}_val'] = attrs[1]
        else:
            contexts.add(f'{alias_fn}str')
            func_name = list(attrs[1].keys())[0]
            line = _get_line(attrs[1], func_name) or line
            statement += self.load_intrinsic_func(f'{alias_fn}str', func_name,
                                                  attrs[1][func_name],
                                                  contexts, line)

        return statement

    def _fn_select(self,
                   resource_id: str,
                   attrs,
                   contexts: set = None,
                   line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::Select."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_select", True)
        contexts.add(alias_fn)

        statement = f"""
            CREATE ({resource_id})-[EXECUTE_FN]->({alias_fn}:Fn:Select {{
                line: ${alias_fn}_line}})-[:HAS]->({alias_fn}idx:Value:Index {{
                    line: ${alias_fn}_line}})
            """
        self.statement_params[f'{alias_fn}_line'] = line

        if isinstance(attrs[0], (str, int)):
            statement += f"SET {alias_fn}idx.value = ${alias_fn}_idx\n"
            self.statement_params[f'{alias_fn}_idx'] = attrs[0]
        else:
            contexts.add(f'{alias_fn}idx')
            func_name = list(attrs[0].keys())[0]
            statement += self.load_intrinsic_func(
                f'{alias_fn}idx', func_name, attrs[0][func_name], contexts,
                _get_line(attrs[0], func_name) or line)

        # add list of values
        statement += f"""
            CREATE ({alias_fn})-[:HAS]->(
                {alias_fn}list:Value:List:ListOfObjects {{
                    line: ${alias_fn}_line}})
            """
        contexts.add(f'{alias_fn}list')
        if isinstance(attrs[1], (OrderedDict, CustomDict)):
            func_name = list(attrs[1].keys())[0]
            statement += self.load_intrinsic_func(
                f'{alias_fn}list', func_name, attrs[1][func_name], contexts,
                _get_line(attrs[1], func_name) or line)

        elif isinstance(attrs[1], (list, CustomList)):
            for idx, value in enumerate(attrs[1]):
                statement += f"""
                    CREATE ({alias_fn}list)-[:HAS]->(
                        {alias_fn}{idx}:Value:Item {{
                            index: {idx}, line:${alias_fn}_line}})
                    """
                if isinstance(value, (str, bool, int)):
                    statement += f"""
                    SET {alias_fn}{idx}.value{idx+1} =${alias_fn}_val{idx+1}
                    """
                    self.statement_params[f'{alias_fn}_val{idx+1}'] = value
                else:
                    contexts.add(f'{alias_fn}{idx}')
                    func_name = list(value.keys())[0]
                    statement += self.load_intrinsic_func(
                        f'{alias_fn}{idx}', func_name, value[func_name],
                        contexts,
                        _get_line(attrs[1][idx], func_name) or line)

        return statement

    def _fn_transform(self,
                      resource_id: str,
                      attrs,
                      contexts: set = None,
                      line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::Transform."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_transform", True)
        contexts.add(alias_fn)

        statement = f"""
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:Fn:Transform {{
                line:${alias_fn}_line}})-[:HAS]->(:Value:Name {{
                    value:${alias_fn}_name, line:${alias_fn}_line}})
            """
        self.statement_params.update({
            f'{alias_fn}_line': line,
            f'{alias_fn}_name': attrs['Name']
        })
        alias_params = create_alias(f'{alias_fn}_parameters', True)
        statement += f"""
            CREATE ({alias_fn})-[:HAS]->({alias_params}:Value:Parameters {{
                line:${alias_fn}_line}})
            """
        contexts.add(alias_params)

        for key, value in attrs['Parameters'].items():
            if key.startswith('__'):
                continue
            param_alias = create_alias(f'{alias_params}_{key}', True)
            statement += f"""
                CREATE ({alias_params})-[:HAS]->(
                    {param_alias}:Value:{create_label(key)} {{
                        line: ${alias_fn}_line}})
                """
            contexts.add(param_alias)
            self.statement_params[f'{param_alias}_name'] = key
            if isinstance(value, (str, int, bool)):
                statement += f"SET {param_alias}.value = ${param_alias}_val\n"
                self.statement_params[f'{param_alias}_val'] = value
            else:
                func_name = list(value.keys())[0]
                line = _get_line(attrs['Parameters'][key], func_name)
                statement += self.load_intrinsic_func(
                    param_alias, func_name, value[func_name], contexts, line)

        return statement

    def _fn_importvalue(self,
                        resource_id: str,
                        attrs,
                        contexts: set = None,
                        line='unknown') -> str:
        """Create a statement to load intrinsic function Fn::ImportValue."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_importvalue", True)
        contexts.add(alias_fn)

        line_sts = f'{{line: ${alias_fn}_line}}'
        statement = (f"CREATE ({resource_id})-[:EXECUTE_FN {line_sts}]->"
                     f"({alias_fn}:Fn:ImportValue)-[:HAS {line_sts}]->"
                     f"({alias_fn}shared:Value:SharedValueToImport)\n")
        self.statement_params[f'{alias_fn}_line'] = line
        contexts.update([alias_fn, f'{alias_fn}shared'])
        if isinstance(attrs, str):
            statement += f" SET {alias_fn}shared.value = ${alias_fn}_value\n"
            self.statement_params[f'{alias_fn}_value'] = attrs
        else:
            func_name = list(attrs.keys())[0]
            line = _get_line(attrs, func_name) or line
            statement += self.load_intrinsic_func(f'{alias_fn}shared',
                                                  func_name, attrs[func_name],
                                                  contexts, line)

        return statement

    def _fn_conditional(self,
                        fn_name: str,
                        resource_id: str,
                        conditions,
                        contexts: set = None,
                        line='unknown') -> str:
        """Create a statement to load conditional funcs."""
        contexts = contexts or set([])
        fn_name_node = fn_name.replace('::', ':')
        alias_fn = create_alias(f'fn_name_node_{resource_id}', True)
        contexts.add(alias_fn)

        statement = f"""
            CREATE ({resource_id})-[:EXECUTE_FN]->({alias_fn}:{fn_name_node} {{
                line: ${alias_fn}_line}})
            """
        self.statement_params[f'{alias_fn}_line'] = line
        if fn_name in ('Fn::if', 'Fn::If'):
            self.statement_params[f'{alias_fn}_con_name'] = conditions[0]
            alias_true = create_alias('true', True)
            alias_false = create_alias('false', True)
            statement += f"""
                SET {alias_fn}.condition_name = ${alias_fn}_con_name
                CREATE ({alias_fn})-[:HAS]->({alias_true}:Value:ValueIfTrue {{
                    line:${alias_fn}_line}})
                CREATE ({alias_fn})-[:HAS]->
                ({alias_false}:ValueValueIfFalse {{line:${alias_fn}_line}})
            """
            contexts.update([alias_true, alias_false])
            # manage value_if_true
            contexts.update([alias_false, alias_true])
            if not isinstance(conditions[1], (OrderedDict, CustomDict)):
                statement += f"""
                            SET {alias_true}.value = ${alias_true}_value
                        """
                self.statement_params[f'{alias_true}_value'] = conditions[1]
            else:
                statement += self._load_resource_property(
                    (alias_true, conditions[1]), contexts, line)
            # manage value_if_false
            if not isinstance(conditions[2], (OrderedDict, CustomDict)):
                statement += f"""
                        SET {alias_false}.value = ${alias_false}_value
                    """
                self.statement_params[f'{alias_false}_value'] = conditions[2]
            else:
                statement += self._load_resource_property(
                    (alias_false, conditions[2]), contexts, line)
            return statement

        for index, con in enumerate(conditions):
            if not isinstance(
                    con, (OrderedDict, dict, list, CustomDict, CustomList)):
                statement += f"""
                        SET {alias_fn}.value{index+1} =
                            $fn_{alias_fn}_value{index+1}
                    """
                self.statement_params[f'fn_{alias_fn}_value{index+1}'] = con
            else:
                func_name = list(con.keys())[0]
                line = _get_line(con, func_name) or line
                statement += self.load_intrinsic_func(
                    alias_fn, func_name, con[func_name], contexts, line)
        return statement

    def _add_attributes_relationship(self,
                                     rel_id,
                                     contexts: set = None,
                                     **kwargs) -> str:
        """Add attributes to a relationship."""
        contexts = contexts or set([])
        contexts_str = ', '.join(contexts)
        statement = ''
        for key, value in kwargs.items():
            statement += f"""
                    WITH {contexts_str}
                    SET {rel_id}.{key} = ${rel_id}_{key}_value
                """
            self.statement_params[f'{rel_id}_{key}_value'] = value
        return statement


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
        count = 1
        for template_path in get_paths(
                path, exclude=exclude, endswith=CLOUDFORMATION_EXTENSIONS):
            with suppress(CloudFormationInvalidTemplateError):
                start_time = timer()
                transaction = Batcher(
                    template_path,
                    connection=self.connection,
                    auto_commit=False)
                print(f'Loading: {template_path}')
                transaction.commit()
                elapsed_time = timer() - start_time
                print('    [SUCCESS]    [%d]  time: %.4f seconds' %
                      (count, elapsed_time))
                count += 1
