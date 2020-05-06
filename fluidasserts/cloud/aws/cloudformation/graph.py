# -*- coding: utf-8 -*-
"""This module provide tools to convert Cloudformation templates in graphs."""

# 3rd party imports
from neo4j import Transaction

# local imports
from fluidasserts.helper.aws import load_cfn_template
from fluidasserts.db.neo4j_connection import ConnectionString, database, runner
from fluidasserts.helper.aws import get_line
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
        statement = ""
        for attr_name, attr_value in param_attrs.items():
            if attr_name.startswith('__'):
                continue
            attr_properties = (
                f"{{name: $param_{param_name}_{attr_name.lower()}_name, "
                f"value: $param_{param_name}_{attr_name.lower()}_value}}")
            statement += (
                f"MERGE ({param_name}_{attr_name.lower()}_:ParameterAttribute"
                f" {attr_properties})\n"
                # create relationship between attribute and parameter
                f"MERGE (param_{param_name.lower()})-"
                f"[rel_{param_name}_{attr_name.lower()}:HAS_ATTRIBUTES]->"
                f"({param_name}_{attr_name.lower()}_)\n"
                f"SET rel_{param_name}_{attr_name.lower()}.line ="
                f" $param_{param_name}_{attr_name.lower()}_line\n")

            try:
                line = param_attrs[f'{attr_name}.line']
            except KeyError:
                line = get_line(param_attrs)

            self.statement_params[
                f'param_{param_name}_{attr_name.lower()}_name'] = attr_name
            attr_value = standardize_objects(
                attr_value)
            self.statement_params[
                f'param_{param_name}_{attr_name.lower()}_value'] = attr_value
            self.statement_params[
                f'param_{param_name}_{attr_name.lower()}_line'] = line
        return statement

    def _load_map_options(self, map_: tuple):
        """Create a statement to create the option nodes of a Mapping."""
        map_name_, map_options = map_
        map_name = map_name_.replace('-', '_')
        statement = ""
        for opt_name_, opt_values in map_options.items():
            if opt_name_.startswith('__'):
                continue
            opt_name = opt_name_.replace('-', '_')
            map_properties = (
                f"{{name: $map_{map_name}_{opt_name.lower()}_name}}")

            statement += (
                f"MERGE ({map_name}_{opt_name.lower()}_:MapOption"
                f" {map_properties})\n"
                f"MERGE (map_{map_name.lower()})-"
                f"[rel_{map_name}_{opt_name.lower()}:HAS_OPTIONS]->"
                f"({map_name}_{opt_name.lower()}_)\n"
                f"SET rel_{map_name}_{opt_name.lower()}.line ="
                f" $map_{map_name}_{opt_name.lower()}_line\n")
            try:
                line = opt_values[f'{opt_name_}.line']
            except KeyError:
                line = get_line(opt_values)
            self.statement_params[
                f'map_{map_name}_{opt_name.lower()}_name'] = opt_name_

            opt_values = standardize_objects(opt_values)
            self.statement_params[
                f'map_{map_name}_{opt_name.lower()}_value'] = opt_values

            self.statement_params[
                f'map_{map_name}_{opt_name.lower()}_line'] = line

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
            # create the node for the parameter
            param_statement = (
                f"MERGE ({alias_parameters})-[:DECLARE_PARAMETER]->"
                f"(param_{param_name.lower()}:Parameter"
                # set attributes of node
                f" {{name: $param_name_{param_name},"
                f" line: $line_param_{param_name}}})\n")
            self.statement_params[f'param_name_{param_name}'] = param_name
            self.statement_params[f'line_param_{param_name}'] = get_line(
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
            map_name = map_name.replace('-', '_')
            if map_name.startswith('__'):
                continue
            map_statement = (f"MERGE ({alias_mappings})-[:DECLARE_MAP]->"
                             f"(map_{map_name.lower()}:Mapping "
                             f"{{name: $map_name_{map_name}, "
                             f"line: $line_map_{map_name}}})\n")
            self.statement_params[f'map_name_{map_name}'] = map_name
            self.statement_params[f'line_map_{map_name}'] = get_line(
                self.template['Mappings'][map_name])

            map_statement += self._load_map_options((map_name, map_options))

            statement += map_statement
        trans.run(statement, **self.statement_params)

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
