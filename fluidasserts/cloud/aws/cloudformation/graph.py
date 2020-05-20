# -*- coding: utf-8 -*-

# pylint: disable=too-many-lines
"""This module provide tools to convert Cloudformation templates in graphs."""

# standar imports
from collections import OrderedDict
from copy import copy

# 3rd party imports
from pyparsing import Char
from pyparsing import nestedExpr
from pyparsing import Optional
from pyparsing import printables
from pyparsing import Suppress
from pyparsing import Word

# local imports
from fluidasserts.db.neo4j_connection import ConnectionString
from fluidasserts.db.neo4j_connection import database
from fluidasserts.db.neo4j_connection import runner
from fluidasserts.helper.aws import _random_string
from fluidasserts.helper.aws import get_line
from fluidasserts.helper.aws import load_cfn_template
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
    alias = name.replace('-', '_').lower()
    alias = alias.replace('::', '_')
    alias = alias.replace(':', '_')
    alias = alias.replace('.', '_')
    if randoms:
        alias = f'{alias}_{_random_string(5)}'
    return alias


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
    return (i[0][0][0] for i in grammar.scanString(expresion))


def _get_line(object_, key):
    line = None
    try:
        line = object_[f'{key}.line']
    except (KeyError, TypeError):
        line = get_line(object_[key])
        if line == 0:
            line = get_line(object_)
    return line if line != 0 else None


class Batcher:  # noqa: H238
    """A class to convert a cloudformation template to graphs."""

    def __init__(self, template_path: str, connection: ConnectionString):
        """Convert an load template.

        Load the template and loop through all the nodes in the document
        to create a statement that loads the nodes to neo4j with their
        relationships.

        :param template_path: File path of CloudFormation template.
        :param connection: Connection parameter and credentials.
        """
        self.path = template_path
        self._load_template_data()
        self.statement_params = {}
        with database(connection) as session:
            session.run('match (n) detach delete n')
            with runner(session) as transactor:
                self.transactor = transactor
                self.create_constraints()
            with runner(session) as transactor:
                self.transactor = transactor
                self.create_template()
                self.load_parameters()
                self.load_mappings()
                self.load_conditions()
                self.load_resources()
                self.load_outputs()

    def _load_template_data(self):
        self.template = load_cfn_template(self.path)

    def create_template(self):
        """Create a node for the template with the basic information."""
        version = self.template.get('AWSTemplateFormatVersion', None)
        description = self.template.get('Description', None)
        alias = self.template['__node_alias__']
        node_name = self.template['__node_name__']

        statement = (f"MERGE ({alias}:{node_name} "
                     "{path: $path, "
                     "AWSTemplateFormatVersion: $version, "
                     "Description: $description})\n")
        self.transactor.run(statement, **{
            'path': self.path,
            'version': version,
            'description': description
        })

    def _load_parameter_attributes(self, parameter: tuple) -> str:
        """Create a statement to create the attribute nodes of a parameter."""
        param_name, param_attrs = parameter
        alias_param = create_alias(param_name)
        statement = ""
        for attr_name, attr_value in param_attrs.items():
            if attr_name.startswith('__'):
                continue
            alias_attr_name = create_alias(attr_name)
            attr_properties = (
                f"{{name: $param_{alias_param}_{alias_attr_name}_name, "
                f"value: $param_{alias_param}_{alias_attr_name}_value}}")
            statement += (
                f"MERGE ({alias_param}_{alias_attr_name}_:ParameterAttribute"
                f" {attr_properties})\n"
                # create relationship between attribute and parameter
                f"MERGE (param_{alias_param})-"
                f"[rel_{alias_param}_{alias_attr_name}:HAS_ATTRIBUTE]->"
                f"({alias_param}_{alias_attr_name}_)\n"
                f"SET rel_{alias_param}_{alias_attr_name}.line ="
                f" $param_{alias_param}_{alias_attr_name}_line\n")

            line = _get_line(param_attrs, attr_name)

            self.statement_params[
                f'param_{alias_param}_{alias_attr_name}_name'] = attr_name
            attr_value = standardize_objects(attr_value)
            self.statement_params[
                f'param_{alias_param}_{alias_attr_name}_value'] = attr_value
            self.statement_params[
                f'param_{alias_param}_{alias_attr_name}_line'] = line
        return statement

    def _load_map_options(self, map_: tuple):
        """Create a statement to create the option nodes of a Mapping."""
        map_name, map_options = map_
        alias_map = create_alias(map_name)
        statement = ""

        for opt_name, opt_values in map_options.items():
            if opt_name.startswith('__'):
                continue
            alias_opt = create_alias(opt_name, True)
            map_properties = (f"{{name: $map_{alias_map}_{alias_opt}_name}}")

            statement += (f"MERGE ({alias_map}_{alias_opt}_:MapOption"
                          f" {map_properties})\n"
                          f"MERGE (map_{alias_map})-"
                          f"[rel_{alias_map}_{alias_opt}:HAS_OPTION]->"
                          f"({alias_map}_{alias_opt}_)\n"
                          f"SET rel_{alias_map}_{alias_opt}.line ="
                          f" $map_{alias_map}_{alias_opt}_line\n")

            line = _get_line(map_options, opt_name)
            self.statement_params[f'map_{alias_map}_{alias_opt}_line'] = line

            self.statement_params[
                f'map_{alias_map}_{alias_opt}_name'] = opt_name
            opt_values = standardize_objects(opt_values)
            for var_name, var_value in opt_values.items():
                if var_name.startswith('__'):
                    continue
                line_var = _get_line(map_options[opt_name], var_name)

                statement += (
                    f"MERGE ({alias_map}_{alias_opt}_)-"
                    f"[rel_{alias_map}_{alias_opt}_{var_name}:HAS_VAR "
                    f"{{line: $rel_{alias_map}_{alias_opt}_{var_name}_line}}]-"
                    f"(:MapVar "
                    f"{{name: ${alias_map}_{alias_opt}_{var_name}_name,"
                    f" value: ${alias_map}_{alias_opt}_{var_name}_value}})\n")
                self.statement_params[
                    f'{alias_map}_{alias_opt}_{var_name}_name'] = var_name
                self.statement_params[
                    f'{alias_map}_{alias_opt}_{var_name}_value'] = var_value
                self.statement_params[
                    f'rel_{alias_map}_{alias_opt}_{var_name}_line'] = line_var
            self.statement_params[
                f'map_{alias_map}_{alias_opt}_value'] = opt_values

        return statement

    def load_parameters(self):
        """Execute a statement that creates the nodes for the template params.

        :param trans: Transaction to execute the statement.
        """
        if 'Parameters' not in self.template.keys():
            return False
        alias_template = self.template['__node_alias__']
        alias_parameters = self.template['Parameters'][
            '__node_alias__'] = "params"

        node_template_name = self.template['__node_name__']
        statement = (f"MATCH ({alias_template}:{node_template_name})\n"
                     f'WHERE {alias_template}.path = "{self.path}"\n'
                     f"CREATE ({alias_template})-"
                     f"[rel_{alias_parameters}:CONTAINS]->"
                     f"({alias_parameters}:Parameters)\n"
                     f"SET rel_{alias_parameters}.line ="
                     f" $rel_{alias_parameters}_line\n")
        self.statement_params[f'rel_{alias_parameters}_line'] = get_line(
            self.template['Parameters'])

        for param_name, param_attrs in self.template['Parameters'].items():
            if param_name.startswith('__'):
                continue
            alias_param = create_alias(param_name)
            # create the node for the parameter
            param_statement = (
                f"CREATE ({alias_parameters})-"
                f"[rel_{alias_param}:DECLARE]->"
                f"(param_{alias_param}:Reference:Parameter"
                # set attributes of node
                f" {{logicalName: $param_name_{alias_param}}})\n"
                f"SET rel_{alias_param}.line = $line_rel_{alias_param}\n")
            self.statement_params[f'param_name_{alias_param}'] = param_name
            self.statement_params[f'line_rel_{alias_param}'] = get_line(
                self.template['Parameters'][param_name])
            # add parameter attributes
            param_statement += self._load_parameter_attributes((param_name,
                                                                param_attrs))

            statement += param_statement

        return self.transactor.run(statement, **self.statement_params)

    def load_mappings(self):
        """Execute a statement that creates nodes for the template Mappings.

        :param trans: Transaction to execute the statement.
        """
        if 'Mappings' not in self.template.keys():
            return False
        alias_mappings = self.template['Mappings'][
            '__node_alias__'] = "mappings"
        alias_template = self.template['__node_alias__']
        node_template_name = self.template['__node_name__']

        statement = (f"MATCH ({alias_template}:{node_template_name})\n"
                     f'WHERE {alias_template}.path = "{self.path}"\n'
                     f"CREATE ({alias_template})-"
                     f"[rel_{alias_mappings}:CONTAINS]->"
                     f"({alias_mappings}:Mappings)\n"
                     f"SET rel_{alias_mappings}.line = "
                     f"$rel_{alias_mappings}_line\n")
        self.statement_params[f'rel_{alias_mappings}_line'] = get_line(
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
            map_statement = (
                f"CREATE ({alias_mappings})-[rel_{alias_map}:DECLARE]->"
                f"(map_{alias_map}:Mapping {{name: $map_name_{alias_map}}})\n"
                f"SET rel_{alias_map}.line = $rel_{alias_map}_line\n")
            self.statement_params[f'map_name_{alias_map}'] = map_name
            self.statement_params[f'rel_{alias_map}_line'] = line

            map_statement += self._load_map_options((map_name, map_options))

            statement += map_statement
        return self.transactor.run(statement, **self.statement_params)

    def load_conditions(self):
        """Execute a statement that creates nodes for the template Conditions.

        :param trans: Transaction to execute the statement.
        """
        if 'Conditions' not in self.template.keys():
            return False
        alias_conditions = self.template['Conditions'][
            '__node_alias__'] = "conditions_node"
        alias_template = self.template['__node_alias__']
        node_template_name = self.template['__node_name__']
        # create relationship between templeate and node conditions
        statement = (
            f"MATCH ({alias_template}:{node_template_name})\n"
            f'WHERE {alias_template}.path = "{self.path}"\n'
            f"CREATE ({alias_template})-[rel_{alias_conditions}:CONTAINS"
            f" {{line: $rel_{alias_conditions}_line}}]->"
            f"({alias_conditions}:Conditions)\n")

        self.statement_params[f'rel_{alias_conditions}_line'] = get_line(
            self.template['Conditions'])

        # Create create relationship between contition nodes and each condition
        for condition_name, condition in self.template['Conditions'].items():
            if condition_name.startswith('__'):
                continue
            if condition_name.startswith('Fn::'):
                contexts = {alias_conditions}
                statement += self.load_intrinsic_func(
                    alias_conditions, condition_name, condition, contexts)
                continue
            alias_con = create_alias(f"con_{condition_name}")
            statement += (f"CREATE ({alias_conditions})-"
                          f"[rel_{alias_con}:DECLARE"
                          f" {{line: $rel_{alias_con}_line}}]->"
                          f"({alias_con}:Condition "
                          f"{{name: $con_name_{alias_con}}})\n")
            self.statement_params[f'con_name_{alias_con}'] = condition_name
            line = _get_line(self.template['Conditions'], condition_name)
            self.statement_params[f'rel_{alias_con}_line'] = line

        self.transactor.run(statement, **self.statement_params)

        # create relationship between the conditions and the functions that
        # each one executes
        for condition_name, condition in self.template['Conditions'].items():
            if condition_name.startswith('__') or condition_name.startswith(
                    'Fn::'):
                continue
            alias_condition = create_alias(f"con_{condition_name}")
            # create reference to condition
            statement_condition = (
                f"MATCH ({alias_condition}:Condition)\n"
                f"WHERE {alias_condition}.name = ${alias_condition}_value\n")
            self.statement_params[f'{alias_condition}_value'] = condition_name
            # create relationship between the condition and the function it
            #  executes
            line = _get_line(self.template['Conditions'], condition_name)
            statement_condition += self._load_condition_funcs(
                (alias_condition, condition), {alias_condition}, line)
            self.transactor.run(statement_condition, **self.statement_params)
        return True

    def load_resources(self):
        """Execute a statement that creates nodes for the template Resources.

        :param trans: Transaction to execute the statement.
        """
        alias_resources = self.template['Resources'][
            '__node_alias__'] = "resources_node"
        alias_template = self.template['__node_alias__']
        node_template_name = self.template['__node_name__']
        # create relationship between templeate and node conditions
        statement = (
            f"MATCH ({alias_template}:{node_template_name})\n"
            f'WHERE {alias_template}.path = "{self.path}"\n'
            f"CREATE ({alias_template})-[rel_{alias_resources}:CONTAINS "
            f"{{line: $rel_{alias_resources}_line}}]->"
            f"({alias_resources}:Resources)\n")
        self.statement_params[f'rel_{alias_resources}_line'] = get_line(
            self.template['Resources'])
        self.transactor.run(statement, **self.statement_params)

        for resource_name in self.template['Resources'].keys():
            if resource_name.startswith(
                    '__') or self.template['Resources'][resource_name].get(
                        '__loaded__', False):
                continue
            self._load_resource(resource_name)

    def load_outputs(self):
        """Execute a statement that creates the nodes for the template Outputs.

        :param trans: Transaction to execute the statement.
        """
        if 'Outputs' not in self.template.keys():
            return False
        alias_outputs = self.template['Outputs'][
            '__node_alias__'] = "resources_node"
        alias_template = self.template['__node_alias__']
        node_template_name = self.template['__node_name__']

        statement = (
            f"MATCH ({alias_template}:{node_template_name})\n"
            f'WHERE {alias_template}.path = "{self.path}"\n'
            f"CREATE ({alias_template})-[rel_{alias_outputs}:CONTAINS "
            f"{{line: $rel_{alias_outputs}_line}}]->"
            f"({alias_outputs}:Outputs)\n")
        self.statement_params[f'rel_{alias_outputs}_line'] = get_line(
            self.template['Outputs'])
        self.transactor.run(statement, **self.statement_params)
        contexts = {alias_outputs}
        for out_name, out_value in self.template['Outputs'].items():
            if out_name.startswith('__'):
                continue
            if out_name.startswith('Fn::'):
                statement += self.load_intrinsic_func(alias_outputs, out_name,
                                                      out_value, contexts)
                continue
            alias_out = create_alias(out_name, True)
            statement += (f"CREATE ({alias_outputs})-"
                          f"[rel_{alias_out}:DECLARE"
                          f" {{line: $rel_{alias_out}_line}}]->"
                          f"({alias_out}:Output "
                          f"{{name: $out_name{alias_out}, "
                          f"Description: $out_desc{alias_out}}})\n")
            contexts.update([alias_out, f'rel_{alias_out}'])
            self.statement_params[f'out_name{alias_out}'] = out_name
            line = _get_line(self.template['Outputs'], out_name)
            self.statement_params[f'rel_{alias_out}_line'] = line
            self.statement_params[f'out_desc{alias_out}'] = out_value.get(
                'Description', 'nothing')
            if isinstance(out_value['Value'], (int, str, bool)):
                statement += f'SET {alias_out}.Value = ${alias_out}_value\n'
                self.statement_params[f'{alias_out}_value'] = out_value[
                    'Value']
            else:
                func_name = list(out_value['Value'].keys())[0]
                line = _get_line(out_value['Value'], func_name)
                statement += self.load_intrinsic_func(
                    alias_out, func_name, out_value['Value'][func_name],
                    contexts, line)
        return self.transactor.run(statement, **self.statement_params)

    def _load_resource(self, resource_name):
        alias_resources = self.template['Resources'][
            '__node_alias__'] = "resources_node"
        alias_template = self.template['__node_alias__']
        node_template_name = self.template['__node_name__']
        resource = self.template['Resources'][resource_name]
        resource_node = resource['Type'].replace('::', ':')
        res_alias = create_alias(resource_name, True)
        contexts = {res_alias}
        statement = (
            f"MATCH ({alias_template}:{node_template_name})-[:CONTAINS]->"
            f"({alias_resources}:Resources)"
            f'WHERE {alias_template}.path = "{self.path}"\n'
            f"CREATE ({alias_resources})-[:DECLARE "
            f"{{line: ${alias_resources}_line}}]->"
            f"({res_alias}:Reference:{resource_node}:{resource_name} {{"
            f"Name:${res_alias}_name, logicalName:${res_alias}_name}})\n")
        self.statement_params[f'{res_alias}_name'] = resource_name
        line = _get_line(self.template['Resources'], resource_name)
        self.statement_params[f'{alias_resources}_line'] = line
        for prop_name, prop_value in resource.get('Properties',
                                                  dict()).items():
            if prop_name.startswith('__'):
                continue
            prop_alias = create_alias(f'{res_alias}_{prop_name}', True)
            line = _get_line(resource['Properties'], prop_name) or line
            contexts.add(prop_alias)

            statement += (
                f"CREATE ({res_alias})-[:HAS {{line: ${prop_alias}_line}}]"
                f"->({prop_alias}:Property:{prop_name} {{"
                f"name: ${prop_alias}_name}})\n")
            self.statement_params[f'{prop_alias}_name'] = prop_name
            self.statement_params[f'{prop_alias}_line'] = line
            statement += self._load_resource_property((prop_alias, prop_value),
                                                      contexts, line)
        self.transactor.run(statement, **self.statement_params)
        self.template['Resources'][resource_name]['__loaded__'] = True

    def _load_resource_property(self,
                                property_: tuple,
                                contexts: set,
                                line='unknown'):
        prop_alias, prop_value = property_
        statement = ""
        if isinstance(prop_value, (str, int, bool)):
            statement += (f"SET {prop_alias}.value = ${prop_alias}_value\n")
            self.statement_params[f'{prop_alias}_value'] = prop_value
        elif isinstance(prop_value, (OrderedDict, CustomDict)):
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
                statement += (f"CREATE ({prop_alias})-"
                              f"[:HAS {{line: ${attr_alias}_line}}]->"
                              f"({attr_alias}:PropertyAttribute:{key})\n")
                self.statement_params[f'{attr_alias}_line'] = line
                statement += self._load_resource_property((attr_alias, value),
                                                          contexts, line)
        elif isinstance(prop_value, (list, CustomList)):
            statement += f"SET {prop_alias} :Array\n"
            for idx, value in enumerate(prop_value):
                alias_item = create_alias(f'{prop_alias}_{idx}', True)
                line = _get_line(prop_value, idx) or line
                statement += (
                    f"CREATE ({prop_alias})-"
                    f"[:HAS {{line: ${alias_item}_line}}]->({alias_item}:Item"
                    f" {{index: {idx}}})\n")
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

    def _create_constraints_template(self):
        self.template['__node_name__'] = 'CloudFormationTemplate'
        self.template['__node_alias__'] = 'template'
        statement = (
            f"CREATE CONSTRAINT ON ({self.template['__node_alias__']}:"
            f"{self.template['__node_name__']}) ASSERT"
            f" {self.template['__node_alias__']}.path IS UNIQUE")
        self.transactor.run(statement)

    def create_constraints(self):
        """Create attribute constraints for nodes."""
        self._create_constraints_template()

    def load_intrinsic_func(self,
                            resource_alias: str,
                            func_name,
                            attrs,
                            contexts: set = None,
                            line='unknown',
                            **kwargs):
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
                   line='unknown',
                   **rel_kwargs):
        """Create a statement to load intrinsic function Fn::Base64."""
        contexts = contexts or set({})
        alias_fn = create_alias("fn_base_base64", True)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = (f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN "
                     f" {{line: ${alias_fn}_line}}]->"
                     f"({alias_fn}: Fn:Base64)\n")
        self.statement_params[f'{alias_fn}_line'] = line
        contexts.add(alias_fn)
        if isinstance(attrs, (str)):
            statement += f"SET {alias_fn}.valueToEncode = ${alias_fn}_value\n"
            self.statement_params[f'{alias_fn}_value'] = attrs
        elif isinstance(attrs, (OrderedDict, CustomDict)):
            for key, _ in attrs.items():
                line = _get_line(attrs, key) or line
                statement += self.load_intrinsic_func(
                    alias_fn, key, attrs[key], contexts, line)
        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)

        return statement

    def _fn_reference(self,
                      resource_id: str,
                      logical_name: str,
                      contexts: set = None,
                      line='unknown',
                      direct_reference=False,
                      **rel_kwargs):
        """Loaf intrinsic function Ref."""
        contexts = contexts or set([])
        ref_alias = create_alias(f'ref_{resource_id}_{logical_name}', True)
        param_alias = create_alias(f'ref_{resource_id}_{logical_name}')
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = ""
        if logical_name in self.template['Resources'].keys(
        ) and '__loaded__' not in self.template['Resources'][logical_name]:
            self._load_resource(logical_name)
        if not direct_reference:
            contexts.update([ref_alias, rel_resource])
            contexts_str = ', '.join(contexts)
            statement += (f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN"
                          f" {{line: ${rel_resource}_lien}}]->"
                          f"({ref_alias}:Ref {{logicalName: "
                          f"${ref_alias}_log_name}})\n"
                          f"WITH {contexts_str}\n")
            self.statement_params[f'{rel_resource}_lien'] = line
        else:
            ref_alias = resource_id
            contexts.add(ref_alias)

        if not logical_name.startswith('AWS::'):
            statement += (
                f"MATCH ({param_alias}: Reference)\n"
                f"WHERE {param_alias}.logicalName = ${param_alias}_name\n"
                f"CREATE ({ref_alias})-[rel_{param_alias}:REFERENCE_TO"
                f" {{line: $rel_{param_alias}_line}}]->"
                f"({param_alias})\n")
            self.statement_params[f'rel_{param_alias}_line'] = line
        else:
            log_id, log_sts = _fn_reference_logincal_id(logical_name)
            statement += (
                f"{log_sts}"
                f"CREATE ({ref_alias})-[rel_{param_alias}:REFERENCE_TO"
                f" {{line: $rel_{param_alias}_line}}]->"
                f"({log_id})\n")

        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)

        self.statement_params[f'rel_{param_alias}_line'] = line
        self.statement_params[f'{ref_alias}_log_name'] = logical_name
        self.statement_params[f'{param_alias}_name'] = logical_name
        return statement

    def _fn_getatt(self,
                   resource_id: str,
                   attrs,
                   contexts: set = None,
                   line='unknown',
                   **rel_kwargs):
        """Create a statement to load intrinsic function Fn::GettAtt."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_getatt", True)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        contexts.update([alias_fn, rel_resource])
        contexts_str = ', '.join(contexts)
        statement = (f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN"
                     f" {{line: ${rel_resource}_line}}]->"
                     f"({alias_fn}:Fn:GetAtt "
                     f"{{logicalNameOfResource: ${alias_fn}_log_name}})\n"
                     f"WITH {contexts_str}\n")
        self.statement_params[f'{rel_resource}_line'] = line
        statement += self._fn_reference(
            alias_fn, attrs[0], contexts, line, direct_reference=True)
        self.statement_params[f'{alias_fn}_log_name'] = attrs[0]
        if not isinstance(attrs[1], (OrderedDict, CustomDict)):
            statement += (
                f"SET {alias_fn}.attributeName = ${alias_fn}_att_name\n")
            self.statement_params[f'{alias_fn}_att_name'] = attrs[1]
        else:
            for key, value in attrs[1].items():
                line = _get_line(attrs[1], key) or line
                statement += self.load_intrinsic_func(alias_fn, key, value,
                                                      contexts, line)
        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)
        return statement

    def _fn_cidr(self,
                 resource_id: str,
                 attrs,
                 contexts: set = None,
                 line='unknown',
                 **rel_kwargs):
        """Create a statement to load intrinsic function Fn::Cidr."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_getatt", True)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = (f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN]->"
                     f"({alias_fn}:Fn:Cidr)\n"
                     f"SET {rel_resource}.line = ${rel_resource}_line\n")
        contexts.update([alias_fn, rel_resource])
        # load ipBlock
        if isinstance(attrs[0], str):
            statement += f"SET {alias_fn}.ipBlock = ${alias_fn}_ipblock\n"
            self.statement_params[f'{alias_fn}_ipblock'] = attrs[0]
        else:
            func_name = list(attrs[0].keys())[0]
            statement += self.load_intrinsic_func(
                alias_fn,
                func_name,
                attrs[0][func_name],
                contexts,
                _get_line(attrs[0], func_name) or line,
                ipBlock=True)
        # load count
        if isinstance(attrs[1], (str, int)):
            statement += f"SET {alias_fn}.count = ${alias_fn}_count\n"
            self.statement_params[f'{alias_fn}_count'] = attrs[1]
        else:
            func_name = list(attrs[1].keys())[0]
            statement += self.load_intrinsic_func(
                alias_fn,
                func_name,
                attrs[1][func_name],
                contexts,
                _get_line(attrs, 1) or line,
                count=True)
        # load cidrBits
        if isinstance(attrs[2], (str, int)):
            statement += f"SET {alias_fn}.cidrBits = ${alias_fn}_cidrbits\n"
            self.statement_params[f'{alias_fn}_cidrbits'] = attrs[2]
        else:
            func_name = list(attrs[2].keys())[0]
            statement += self.load_intrinsic_func(
                alias_fn,
                func_name,
                attrs[2][func_name],
                contexts,
                _get_line(attrs[2], func_name) or line,
                cidrBits=True)

        self.statement_params[f'{rel_resource}_line'] = line

        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)
        return statement

    def _fn_find_in_map(self,
                        resource_id: str,
                        attrs,
                        contexts: set = None,
                        line='unknown',
                        **rel_kwargs):
        """Create a statement to load intrinsic function Fn::FindInMap."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_findinmap", True)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = (f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN "
                     f"{{line: ${rel_resource}_line}}]->"
                     f"({alias_fn}:Fn:FindInMap)\n")
        self.statement_params[f'{rel_resource}_line'] = line
        contexts.update([alias_fn, rel_resource])

        # load mapname
        statement += f"SET ({alias_fn}).MapName = ${alias_fn}_mapname\n"
        self.statement_params[f'{alias_fn}_mapname'] = attrs[0]

        if isinstance(attrs[1], (str)):
            statement += f"SET {alias_fn}.TopLevelKey = ${alias_fn}_top\n"
            self.statement_params[f'{alias_fn}_top'] = attrs[1]
        else:
            func_name = list(attrs[1].keys())[0]
            statement += self.load_intrinsic_func(
                alias_fn,
                func_name,
                attrs[1][func_name],
                contexts,
                _get_line(attrs[1], func_name) or line,
                TopLevelKey=True)

        if isinstance(attrs[2], (str)):
            statement += f"SET {alias_fn}.SecondLevelKey = ${alias_fn}_sec\n"
            self.statement_params[f'{alias_fn}_sec'] = attrs[2]
        else:
            func_name = list(attrs[2].keys())[0]
            statement += self.load_intrinsic_func(
                alias_fn,
                func_name,
                attrs[2][func_name],
                contexts,
                _get_line(attrs[2], func_name) or line,
                SecondLevelKey=True)

        contexts_str = ', '.join(contexts)

        alias_mapping = create_alias(f'{attrs[0]}_mapping', True)
        contexts1 = contexts
        contexts1.add(alias_mapping)
        contexts_str1 = ', '.join(contexts1)
        statement += (
            f"WITH {contexts_str}\n"
            f"MATCH ({alias_mapping}:Mapping)\n"
            f"WHERE {alias_mapping}.name = ${alias_mapping}_name\n"
            f"WITH {contexts_str1}\n"
            f"CREATE ({alias_fn})-[:REFERENCE_TO]->({alias_mapping})\n")
        self.statement_params[f'{alias_mapping}_name'] = attrs[0]

        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)
        return statement

    def _fn_get_azs(self,
                    resource_id: str,
                    attrs,
                    contexts: set = None,
                    line='unknown',
                    **rel_kwargs):
        """Create a statement to load intrinsic function Fn::GetAZs."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_getazs", True)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = (
            f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN "
            f"{{line: ${rel_resource}_line}}]->({alias_fn}:Fn:GetZAs)\n")
        self.statement_params[f'{rel_resource}_line'] = line
        contexts.add(alias_fn)
        if isinstance(attrs, str):
            statement += f"SET {alias_fn}.region = ${alias_fn}_region\n"
            self.statement_params[f'{alias_fn}_region'] = attrs
        else:
            func_name = list(attrs.keys())[0]
            line = _get_line(attrs, func_name) or line
            statement += self.load_intrinsic_func(
                alias_fn,
                func_name,
                attrs[func_name],
                contexts,
                line,
                region=True)

        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)
        return statement

    def _fn_sub(self,
                resource_id: str,
                attrs,
                contexts: set = None,
                line='unknown',
                **rel_kwargs):
        """Create a statement to load intrinsic function Fn::Sub."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_sub", True)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = (f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN "
                     f"{{line: ${rel_resource}_line}}]->({alias_fn}:Fn:Sub"
                     f" {{String: ${alias_fn}_string}})\n")
        self.statement_params[f'{rel_resource}_line'] = line
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
                    # pending handling references to resource attributes
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
                statement += (
                    f"CREATE ({alias_fn})-[:REFERENCE_TO]->"
                    f"({alias_var }:Var {{name: ${alias_fn}_{key}_name}})\n")
                contexts.add(alias_var)
                self.statement_params[f'{alias_fn}_{key}_name'] = key

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

        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)
        return statement

    def _fn_join(self,
                 resource_id: str,
                 attrs,
                 contexts: set = None,
                 line='unknown',
                 **rel_kwargs):
        """Create a statement to load intrinsic function Fn::Join."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_join", True)
        contexts.add(alias_fn)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = (f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN "
                     f"{{line: ${rel_resource}_line}}]->({alias_fn}:Fn:Join"
                     f" {{delimiter: ${alias_fn}_delimiter}})\n")
        self.statement_params[f'{alias_fn}_delimiter'] = attrs[0]
        self.statement_params[f'{rel_resource}_line'] = line

        for idx, value in enumerate(attrs[1]):
            if isinstance(value, (str, bool, int)):
                statement += (
                    f"SET {alias_fn}.value{idx+1} = ${alias_fn}_val{idx+1}\n")
                self.statement_params[f'{alias_fn}_val{idx+1}'] = value
            else:
                func_name = list(value.keys())[0]
                line = _get_line(attrs[1][idx], func_name) or line
                statement += self.load_intrinsic_func(
                    alias_fn, func_name, value[func_name], contexts, line, **{
                        f'value{idx+1}': True
                    })

        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)

        return statement

    def _fn_split(self,
                  resource_id: str,
                  attrs,
                  contexts: set = None,
                  line='unknown',
                  **rel_kwargs):
        """Create a statement to load intrinsic function Fn::Split."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_split", True)
        contexts.add(alias_fn)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = (f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN "
                     f"{{line: ${rel_resource}_line}}]->({alias_fn}:Fn:Split"
                     f" {{delimiter: ${alias_fn}_delimiter}})\n")
        self.statement_params[f'{alias_fn}_delimiter'] = attrs[0]
        self.statement_params[f'{rel_resource}_line'] = line

        if isinstance(attrs[1], (str, bool, int)):
            statement += (f"SET {alias_fn}.source_string = ${alias_fn}_val\n")
            self.statement_params[f'{alias_fn}_val'] = attrs[1]
        else:
            func_name = list(attrs[1].keys())[0]
            line = _get_line(attrs[1], func_name) or line
            statement += self.load_intrinsic_func(
                alias_fn, func_name, attrs[1][func_name], contexts, line)

        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)

        return statement

    def _fn_select(self,
                   resource_id: str,
                   attrs,
                   contexts: set = None,
                   line='unknown',
                   **rel_kwargs):
        """Create a statement to load intrinsic function Fn::Select."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_select", True)
        contexts.add(alias_fn)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = (
            f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN "
            f"{{line: ${rel_resource}_line}}]->({alias_fn}:Fn:Select)")
        self.statement_params[f'{rel_resource}_line'] = line

        if isinstance(attrs[0], (str, int)):
            statement += (f"SET {alias_fn}.index = ${alias_fn}_val\n")
            self.statement_params[f'{alias_fn}_val'] = attrs[0]
        else:
            func_name = list(attrs[0].keys())[0]
            statement += self.load_intrinsic_func(
                alias_fn,
                func_name,
                attrs[0][func_name],
                contexts,
                _get_line(attrs[0], func_name) or line,
                index=True)

        if isinstance(attrs[1], (OrderedDict, CustomDict)):
            func_name = list(attrs[1].keys())[0]
            statement += self.load_intrinsic_func(
                alias_fn,
                func_name,
                attrs[1][func_name],
                contexts,
                _get_line(attrs[1], func_name) or line,
                index=True)

        elif isinstance(attrs[1], (list, CustomList)):
            for idx, value in enumerate(attrs[1]):
                if isinstance(value, (str, bool, int)):
                    statement += (f"SET {alias_fn}.value{idx+1} ="
                                  f" ${alias_fn}_val{idx+1}\n")
                    self.statement_params[f'{alias_fn}_val{idx+1}'] = value
                else:
                    func_name = list(value.keys())[0]
                    statement += self.load_intrinsic_func(
                        alias_fn, func_name, value[func_name], contexts,
                        _get_line(attrs[1][idx], func_name) or line, **{
                            f'value{idx+1}': True
                        })

        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)

        return statement

    def _fn_transform(self,
                      resource_id: str,
                      attrs,
                      contexts: set = None,
                      line='unknown',
                      **rel_kwargs):
        """Create a statement to load intrinsic function Fn::Transform."""
        contexts = contexts or set([])
        alias_fn = create_alias("fn_transform", True)
        contexts.add(alias_fn)
        rel_resource = create_alias(f'rel_{resource_id}', True)
        statement = (f"CREATE ({resource_id})-[{rel_resource}:EXECUTE_FN "
                     f"{{line: ${rel_resource}_line}}]->"
                     f"({alias_fn}:Fn:Transform {{Name: ${alias_fn}_name}})\n")
        self.statement_params[f'{rel_resource}_line'] = line
        self.statement_params[f'{alias_fn}_name'] = attrs['Name']
        alias_params = create_alias(f'{alias_fn}_parameters', True)
        statement += (
            f"CREATE ({alias_fn})-[:HAS]->({alias_params}:Parameters)\n")

        for key, value in attrs['Parameters'].items():
            if key.startswith('__'):
                continue
            param_alias = create_alias(f'{alias_params}_{key}', True)
            statement += (
                f"CREATE ({alias_params})-[:HAS_ATTRIBUTE]->"
                f"({param_alias}:FnAttribute {{name: ${param_alias}_name}})\n")
            self.statement_params[f'{param_alias}_name'] = key
            if isinstance(value, (str, int, bool)):
                statement += (
                    f"SET {param_alias}.value = ${param_alias}_val\n")
                self.statement_params[f'{param_alias}_val'] = value
            else:
                func_name = list(value.keys())[0]
                line = _get_line(attrs['Parameters'][key], func_name)
                statement += self.load_intrinsic_func(
                    alias_fn, func_name, value[func_name], contexts, line)

        if rel_kwargs:
            contexts.add(rel_resource)
            statement += self._add_attributes_relationship(
                rel_resource, contexts, **rel_kwargs)

        return statement

    def _fn_conditional(self,
                        fn_name: str,
                        resource_id: str,
                        conditions,
                        contexts: set = None,
                        line='unknown',
                        **rel_kwargs):
        """Create a statement to load conditional funcs."""
        contexts = contexts or set([])
        fn_name_node = fn_name.replace('::', ':')
        alias_fn = create_alias(f'fn_name_node_{resource_id}', True)
        alias_rel = create_alias(f'rel_{alias_fn}', True)
        contexts.add(alias_fn)
        statement = (f"CREATE ({resource_id})-"
                     f"[{alias_rel}:EXECUTE_FN {{line: ${alias_rel}_line}}]->"
                     f"({alias_fn}:{fn_name_node})\n")
        self.statement_params[f'{alias_rel}_line'] = line
        if rel_kwargs:
            contexts.add(alias_rel)
            statement += self._add_attributes_relationship(
                alias_rel, contexts, **rel_kwargs)
        if fn_name in ('Fn::if', 'Fn:If'):
            statement += (
                f"SET {alias_fn}.condition_name = ${alias_fn}_con_name\n")
            self.statement_params[f'{alias_fn}_con_name'] = conditions[0]
            # manage value_if_true
            if not isinstance(conditions[1], (OrderedDict, CustomDict)):
                statement += (f"SET {alias_fn}.value_if_true = "
                              f"$fn_{alias_fn}_value_is_true\n")
                self.statement_params[
                    f'fn_{alias_fn}_value_is_true'] = conditions[1]
            else:
                func_name = list(conditions[1].keys())[0]
                statement += self.load_intrinsic_func(
                    alias_fn,
                    func_name,
                    conditions[1][func_name],
                    contexts,
                    _get_line(conditions[1], func_name) or line,
                    value_if_true=True)
            # manage value_if_true
            if not isinstance(conditions[2], (OrderedDict, CustomDict)):
                statement += (f"SET {alias_fn}.value_if_false = "
                              f"$fn_{alias_fn}_value_is_false\n")
                self.statement_params[
                    f'fn_{alias_fn}_value_is_false'] = conditions[2]
            else:
                func_name = list(conditions[2].keys())[0]
                statement += self.load_intrinsic_func(
                    alias_fn,
                    func_name,
                    conditions[2][func_name],
                    contexts,
                    _get_line(conditions[2], func_name) or line,
                    value_if_false=True)
            return statement

        for index, con in enumerate(conditions):
            if not isinstance(
                    con, (OrderedDict, dict, list, CustomDict, CustomList)):
                statement += (f"SET {alias_fn}.value{index+1} = "
                              f"$fn_{alias_fn}_value{index+1}\n")
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
                                     **kwargs):
        """Add attributes to a relationship."""
        contexts = contexts or set([])
        contexts_str = ', '.join(contexts)
        statement = ''
        for key, value in kwargs.items():
            statement += (f"WITH {contexts_str}\n"
                          f"SET {rel_id}.{key} = ${rel_id}_{key}_value\n")
            self.statement_params[f'{rel_id}_{key}_value'] = value
        return statement
