# -*- coding: utf-8 -*-
"""This module provide tools to convert Cloudformation templates in graphs."""

# standar imports
from collections import OrderedDict

# 3rd party imports
from neo4j import Transaction

# local imports
from fluidasserts.helper.aws import load_cfn_template
from fluidasserts.db.neo4j_connection import ConnectionString, database, runner
from fluidasserts.helper.aws import get_line, _random_string
from fluidasserts.utils.parsers.json import standardize_objects


class Batcher():
    """A class to convert a cloudformation template to graphs."""

    def __init__(self, template_path: str, connection: ConnectionString):
        """
        Convert an load template.

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
            with runner(session) as transactor:
                self.create_constraints(transactor)
            with runner(session) as transactor:
                self.create_template(transactor)
                self.load_parameters(transactor)
                self.load_mappings(transactor)
                self.load_conditions(transactor)

    def _load_template_data(self):
        self.template = load_cfn_template(self.path)

    def create_template(self, trans: Transaction):
        """Create a node for the template with the basic information."""
        version = self.template.get('AWSTemplateFormatVersion', None)
        description = self.template.get('Description', None)
        alias = self.template['__node_alias__']
        node_name = self.template['__node_name__']

        statement = (f"MERGE ({alias}:{node_name} "
                     "{path: $path, "
                     "AWSTemplateFormatVersion: $version, "
                     "Description: $description})\n")
        trans.run(statement, **{
            'path': self.path,
            'version': version,
            'description': description
        })

    def _load_parameter_attributes(self, parameter: tuple) -> str:
        """Create a statement to create the attribute nodes of a parameter."""
        param_name, param_attrs = parameter
        alias_param = param_name.replace('-', '_').lower()
        statement = ""
        for attr_name, attr_value in param_attrs.items():
            if attr_name.startswith('__'):
                continue
            alias_attr_name = attr_name.replace('-', '_').lower()
            attr_properties = (
                f"{{name: $param_{alias_param}_{alias_attr_name}_name, "
                f"value: $param_{alias_param}_{alias_attr_name}_value}}")
            statement += (
                f"MERGE ({alias_param}_{alias_attr_name}_:ParameterAttribute"
                f" {attr_properties})\n"
                # create relationship between attribute and parameter
                f"MERGE (param_{alias_param})-"
                f"[rel_{alias_param}_{alias_attr_name}:HAS_ATTRIBUTES]->"
                f"({alias_param}_{alias_attr_name}_)\n"
                f"SET rel_{alias_param}_{alias_attr_name}.line ="
                f" $param_{alias_param}_{alias_attr_name}_line\n")

            try:
                line = param_attrs[f'{attr_name}.line']
            except KeyError:
                line = get_line(param_attrs)

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
        alias_map = map_name.replace('-', '_').lower()
        statement = ""
        for opt_name, opt_values in map_options.items():
            if opt_name.startswith('__'):
                continue
            alias_opt = opt_name.replace('-', '_').lower()
            map_properties = (f"{{name: $map_{alias_map}_{alias_opt}_name}}")

            statement += (
                f"MERGE ({alias_map}_{alias_opt}_:MapOption"
                f" {map_properties})\n"
                f"MERGE (map_{alias_map})-"
                f"[rel_{alias_map}_{alias_opt}:HAS_OPTIONS]->"
                f"({alias_map}_{alias_opt}_)\n"
                f"SET rel_{alias_map}_{alias_opt}.line ="
                f" $map_{alias_map}_{alias_opt}_line\n")
            try:
                line = opt_values[f'{opt_name}.line']
            except KeyError:
                line = get_line(opt_values)
            self.statement_params[
                f'map_{alias_map}_{alias_opt}_name'] = opt_name

            opt_values = standardize_objects(opt_values)
            self.statement_params[
                f'map_{alias_map}_{alias_opt}_value'] = opt_values

            self.statement_params[f'map_{alias_map}_{alias_opt}_line'] = line

        return statement

    def load_parameters(self, trans: Transaction):
        """
        Execute a statement that creates the nodes for the template params.

        :param trans: Transaction to execute the statement.
        """
        alias_template = self.template['__node_alias__']
        alias_parameters = self.template['Parameters'][
            '__node_alias__'] = "params"

        self.statement_params['line_node_parameters'] = get_line(
            self.template['Parameters'])

        node_template_name = self.template['__node_name__']
        statement = (f"MATCH ({alias_template}:{node_template_name})\n"
                     f'WHERE {alias_template}.path = "{self.path}"\n'
                     f"MERGE ({alias_template})-[:CONTAINS]->"
                     f"({alias_parameters}:Parameters"
                     " {line: $line_node_parameters})\n")

        for param_name, param_attrs in self.template['Parameters'].items():
            if param_name.startswith('__'):
                continue
            alias_param = param_name.replace('-', '_').lower()
            # create the node for the parameter
            param_statement = (
                f"MERGE ({alias_parameters})-[:DECLARE_PARAMETER]->"
                f"(param_{alias_param}:Parameter"
                # set attributes of node
                f" {{name: $param_name_{alias_param},"
                f" line: $line_param_{alias_param}}})\n")
            self.statement_params[f'param_name_{alias_param}'] = param_name
            self.statement_params[f'line_param_{alias_param}'] = get_line(
                self.template['Parameters'][param_name])
            # add parameter attributes
            param_statement += self._load_parameter_attributes((param_name,
                                                                param_attrs))

            statement += param_statement

        trans.run(statement, **self.statement_params)

    def load_mappings(self, trans: Transaction):
        """
        Execute a statement that creates the nodes for the template Mappings.

        :param trans: Transaction to execute the statement.
        """
        alias_mappings = self.template['Mappings'][
            '__node_alias__'] = "mappings"
        alias_template = self.template['__node_alias__']
        node_template_name = self.template['__node_name__']

        statement = (f"MATCH ({alias_template}:{node_template_name})\n"
                     f'WHERE {alias_template}.path = "{self.path}"\n'
                     f"MERGE ({alias_template})-[:CONTAINS]->"
                     f"({alias_mappings}:Mappings"
                     " {line: $line_node_parameters})\n")
        self.statement_params['line_node_mappings'] = get_line(
            self.template['Mappings'])

        for map_name, map_options in self.template['Mappings'].items():
            if map_name.startswith('__'):
                continue
            alias_map = map_name.replace('-', '_').lower()
            map_statement = (
                f"MERGE ({alias_mappings})-[:DECLARE_MAP]->"
                f"(map_{alias_map}:Mapping {{name: $map_name_{alias_map}, "
                f"line: $line_map_{alias_map}}})\n")
            self.statement_params[f'map_name_{alias_map}'] = map_name
            self.statement_params[f'line_map_{alias_map}'] = get_line(
                self.template['Mappings'][map_name])

            map_statement += self._load_map_options((map_name, map_options))

            statement += map_statement
        trans.run(statement, **self.statement_params)

    def load_conditions(self, trans: Transaction):
        """
        Execute a statement that creates the nodes for the template Conditions.

        :param trans: Transaction to execute the statement.
        """
        alias_conditions_f = self.template['Conditions'][
            '__node_alias__'] = "conditions_node"
        alias_template = self.template['__node_alias__']
        node_template_name = self.template['__node_name__']
        # create relationship between templeate and node conditions
        statement = (
            f"MATCH ({alias_template}:{node_template_name})\n"
            f'WHERE {alias_template}.path = "{self.path}"\n'
            f"MERGE ({alias_template})-[:CONTAINS]->"
            f"({alias_conditions_f}:Conditions"
            " {line: $line_node_parameters})\n")
        self.statement_params['line_node_conditions'] = get_line(
            self.template['Conditions'])

        # Create create relationship between contition nodes and each condition
        for condition_name, condition in self.template['Conditions'].items():
            if condition_name.startswith('__'):
                continue
            alias_condition = f"con_{condition_name.replace('-', '_').lower()}"
            statement += (
                f"MERGE ({alias_conditions_f})-[:DECLARE_CONDITION]->"
                f"({alias_condition}:Condition "
                f"{{name: $con_name_{alias_condition}, "
                f"line: $line_con_{alias_condition}}})\n")
            self.statement_params[
                f'con_name_{alias_condition}'] = condition_name
            self.statement_params[f'line_con_{alias_condition}'] = get_line(
                self.template['Conditions'][condition_name])

        trans.run(statement, **self.statement_params)

        # create relationship between the conditions and the functions that
        # each one executes
        for condition_name, condition in self.template['Conditions'].items():
            if condition_name.startswith('__'):
                continue
            alias_condition = f"con_{condition_name.replace('-', '_').lower()}"
            # create reference to condition
            statement_condition = (
                f"MATCH ({alias_condition}:Condition)\n"
                f"WHERE {alias_condition}.name = ${condition_name}_value\n"
                f"WITH {alias_condition}\n")
            self.statement_params[f'{condition_name}_value'] = condition_name
            # create relationship between the condition and the function it
            #  executes
            statement_condition += self._load_condition_funcs(
                (alias_condition, condition), {alias_condition})
            trans.run(statement_condition, **self.statement_params)

    def _load_condition_funcs(self, func: tuple, context: set) -> str:
        """
        Create a statement to load a function.

        Context lets inherit contexts from top nodes to create relationships.
        :param func: Function to load.
        :param context: Context to execute statements.
        """
        alias_f, func_exc = func
        fn_name = list(func_exc.keys())[0]

        # if the function is a reference it creates the relationship with
        # the parameter
        if fn_name == 'Ref':
            reference = func_exc['Ref']
            self.statement_params[
                f'ref_{alias_f}_{reference}_name'] = reference
            # add node to context
            context.update([f'ref_{alias_f}_{reference}', alias_f])
            contexts_str = ', '.join(context)

            return (
                f"MATCH (ref_{alias_f}_{reference}: Parameter)\n"
                f"WHERE ref_{alias_f}_{reference}.name = "
                f"$ref_{alias_f}_{reference}_name\n"
                f"WITH {contexts_str}\n"
                f"MERGE ({alias_f})-[:REFERENCE_TO]->"
                f"(ref_{alias_f}_{reference})\n"
                f"WITH {contexts_str}\n")

        fn_name_node = fn_name.replace('::', ':')
        alias_fn_name = fn_name_node.lower().replace(':', '_')
        alias_fn_node = f'fn_{alias_f}_{alias_fn_name}_{_random_string(5)}'
        # add node to context
        context.update([alias_fn_node, alias_f])
        contexts_str = ', '.join(context)

        # create relationship with condition
        statement = (f"CREATE ({alias_f})-"
                     f"[rel_{alias_f}_{alias_fn_name}:EXCECUTE_FN]->"
                     f"({alias_fn_node}:{fn_name_node})\n"
                     f"WITH {contexts_str}\n")
        # add function parameters
        for param in func_exc[fn_name]:
            if not isinstance(param, (OrderedDict, dict, list)):
                statement += (f"SET {alias_fn_node}.param_value = "
                              f"$fn_{alias_f}_{alias_fn_name}_value\n")
                self.statement_params[
                    f'fn_{alias_f}_{alias_fn_name}_value'] = param
            else:
                # if the parameter is a function it makes a recursive call
                statement += self._load_condition_funcs(
                    (f'{alias_fn_node}', param), context)
        return statement

    def _create_constraints_template(self, trans: Transaction):
        self.template['__node_name__'] = 'CloudFormationTemplate'
        self.template['__node_alias__'] = 'template'
        statement = (
            f"CREATE CONSTRAINT ON ({self.template['__node_alias__']}:"
            f"{self.template['__node_name__']}) ASSERT"
            f" {self.template['__node_alias__']}.path IS UNIQUE")
        trans.run(statement)

    def create_constraints(self, trans: Transaction):
        """Create attribute constraints for nodes."""
        self._create_constraints_template(trans)
