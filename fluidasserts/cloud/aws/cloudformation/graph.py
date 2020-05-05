# -*- coding: utf-8 -*-
"""This module provide tools to convert Cloudformation templates in graphs."""

# 3rd party imports
from neo4j import Transaction

# local imports
from fluidasserts.helper.aws import load_cfn_template
from fluidasserts.db.neo4j_connection import ConnectionString, database, runner
from fluidasserts.helper.aws import get_line
from fluidasserts.utils.parsers.json import CustomList


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

    def _load_parameter_attributes(self, parameter) -> str:
        """Create a statement to create the attribute nodes of a parameter."""
        param_name, param_attrs = parameter
        statement = ""
        for attr_name, attr_value in param_attrs.items():
            if attr_name.startswith('__'):
                continue
            attr_properties = (
                f"{{name: $param_{param_name}_{attr_name.lower()}_name, "
                f"value: $param_{param_name}_{attr_name.lower()}_value, "
                f"line: $param_{param_name}_{attr_name.lower()}_line}}")
            statement += (
                f"MERGE ({param_name}_{attr_name.lower()}_:ParameterAttribute"
                f" {attr_properties})\n"
                # create relationship between attribute and parameter
                f"MERGE (param_{param_name.lower()})-[:HAS_ATTRIBUTES]->"
                f"({param_name}_{attr_name.lower()}_)\n")

            try:
                line = param_attrs[f'{attr_name}.line']
            except KeyError:
                line = get_line(param_attrs)

            if isinstance(attr_value, CustomList):
                attr_value = list(attr_value)
            self.statement_params[
                f'param_{param_name}_{attr_name.lower()}_name'] = attr_name
            self.statement_params[
                f'param_{param_name}_{attr_name.lower()}_value'] = attr_value
            self.statement_params[
                f'param_{param_name}_{attr_name.lower()}_line'] = line
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
        statement = (f"MATCH ({alias_template.lower()}:{node_template_name})\n"
                     f'WHERE {alias_template.lower()}.path = "{self.path}"\n'
                     f"MERGE ({alias_template.lower()})-[:CONTAINS]->"
                     f"({alias_parameters.lower()}:Parameters"
                     " {line: $line_node_parameters})\n")

        for param_name, param_attrs in self.template['Parameters'].items():
            if param_name.startswith('__'):
                continue
            # create the node for the parameter
            param_statement = (
                f"MERGE ({alias_parameters.lower()})-[:DECLARE_PARAMETER]->"
                f"(param_{param_name.lower()}:Parameter"
                # set attributes of node
                f" {{name: $value_param_name_{param_name},"
                f" line: $line_node_param_{param_name}}})\n")
            self.statement_params[
                f'value_param_name_{param_name}'] = param_name
            self.statement_params[f'line_node_param_{param_name}'] = get_line(
                self.template['Parameters'][f'{param_name}'])
            # add parameter attributes
            param_statement += self._load_parameter_attributes((param_name,
                                                                param_attrs))

            statement += param_statement

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
