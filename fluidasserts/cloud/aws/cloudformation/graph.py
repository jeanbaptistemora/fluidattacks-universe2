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
from fluidasserts.utils.parsers.json import CustomDict

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
    'Ref'
]


def create_alias(name: str, randoms=False) -> str:
    """
    Create an alias for Cipher statement.

    :param randoms: Add random chars to alias.
    """
    alias = name.replace('-', '_').lower()
    alias = alias.replace('::', '_')
    alias = alias.replace(':', '_')
    if randoms:
        alias = f'{alias}_{_random_string(5)}'
    return alias


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
            session.run('match (n) detach delete n')
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
        alias_map = create_alias(map_name)
        statement = ""
        for opt_name, opt_values in map_options.items():
            if opt_name.startswith('__'):
                continue
            alias_opt = create_alias(opt_name)
            map_properties = (f"{{name: $map_{alias_map}_{alias_opt}_name}}")

            statement += (
                f"MERGE ({alias_map}_{alias_opt}_:MapOption"
                f" {map_properties})\n"
                f"MERGE (map_{alias_map})-"
                f"[rel_{alias_map}_{alias_opt}:HAS_OPTION]->"
                f"({alias_map}_{alias_opt}_)\n"
                f"SET rel_{alias_map}_{alias_opt}.line ="
                f" $map_{alias_map}_{alias_opt}_line\n")

            line = get_line(map_options[opt_name])

            self.statement_params[
                f'map_{alias_map}_{alias_opt}_name'] = opt_name

            opt_values = standardize_objects(opt_values)
            for var_name, var_value in opt_values.items():
                if var_name.startswith('__'):
                    continue
                try:
                    line_var = map_options[opt_name][f'{var_name}.line']
                except KeyError:
                    line_var = get_line(map_options[opt_name])

                statement += (
                    f"MERGE ({alias_map}_{alias_opt}_)-"
                    f"[rel_{alias_map}_{alias_opt}_{var_name}:HAS_VAR]-"
                    f"(:MapVar "
                    f"{{name: ${alias_map}_{alias_opt}_{var_name}_name,"
                    f" value: ${alias_map}_{alias_opt}_{var_name}_value}})"
                    f"SET rel_{alias_map}_{alias_opt}_{var_name}.line ="
                    f"$rel_{alias_map}_{alias_opt}_{var_name}_line\n")
                self.statement_params[
                    f'{alias_map}_{alias_opt}_{var_name}_name'] = var_name
                self.statement_params[
                    f'{alias_map}_{alias_opt}_{var_name}_value'] = var_value
                self.statement_params[
                    f'rel_{alias_map}_{alias_opt}_{var_name}_line'] = line_var
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
                f"[rel_{alias_param}:DECLARE_PARAMETER]->"
                f"(param_{alias_param}:Parameter"
                # set attributes of node
                f" {{name: $param_name_{alias_param}}})\n"
                f"SET rel_{alias_param}.line = $line_rel_{alias_param}\n")
            self.statement_params[f'param_name_{alias_param}'] = param_name
            self.statement_params[f'line_rel_{alias_param}'] = get_line(
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
            alias_map = create_alias(map_name)
            map_statement = (
                f"CREATE ({alias_mappings})-[rel_{alias_map}:DECLARE_MAP]->"
                f"(map_{alias_map}:Mapping {{name: $map_name_{alias_map}}})\n"
                f"SET rel_{alias_map}.line = $rel_{alias_map}_line\n")
            self.statement_params[f'map_name_{alias_map}'] = map_name
            self.statement_params[f'rel_{alias_map}_line'] = get_line(
                self.template['Mappings'][map_name])

            map_statement += self._load_map_options((map_name, map_options))

            statement += map_statement
        trans.run(statement, **self.statement_params)

    def load_conditions(self, trans: Transaction):
        """
        Execute a statement that creates the nodes for the template Conditions.

        :param trans: Transaction to execute the statement.
        """
        alias_conditions = self.template['Conditions'][
            '__node_alias__'] = "conditions_node"
        alias_template = self.template['__node_alias__']
        node_template_name = self.template['__node_name__']
        # create relationship between templeate and node conditions
        statement = (
            f"MATCH ({alias_template}:{node_template_name})\n"
            f'WHERE {alias_template}.path = "{self.path}"\n'
            f"CREATE ({alias_template})-[rel_{alias_conditions}:CONTAINS]->"
            f"({alias_conditions}:Conditions)\n"
            f"SET rel_{alias_conditions}.line = $rel_{alias_conditions}_line\n"
        )

        self.statement_params[f'rel_{alias_conditions}_line'] = get_line(
            self.template['Conditions'])

        # Create create relationship between contition nodes and each condition
        for condition_name, condition in self.template['Conditions'].items():
            if condition_name.startswith('__'):
                continue
            alias_con = create_alias(f"con_{condition_name}")
            statement += (
                f"CREATE ({alias_conditions})-"
                f"[rel_{alias_con}:DECLARE_CONDITION]->"
                f"({alias_con}:Condition "
                f"{{name: $con_name_{alias_con}}})\n"
                f"SET rel_{alias_con}.line = $rel_{alias_con}_line\n")
            self.statement_params[f'con_name_{alias_con}'] = condition_name
            self.statement_params[f'rel_{alias_con}_line'] = get_line(
                self.template['Conditions'][condition_name])

        trans.run(statement, **self.statement_params)

        # create relationship between the conditions and the functions that
        # each one executes
        for condition_name, condition in self.template['Conditions'].items():
            if condition_name.startswith('__'):
                continue
            alias_condition = create_alias(f"con_{condition_name}")
            # create reference to condition
            statement_condition = (
                f"MATCH ({alias_condition}:Condition)\n"
                f"WHERE {alias_condition}.name = ${alias_condition}_value\n"
                f"WITH {alias_condition}\n")
            self.statement_params[f'{alias_condition}_value'] = condition_name
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

        if fn_name in INTRINSIC_FUNCS:
            try:
                line = func_exc[f'{fn_name}.line']
            except KeyError:
                line = 'unknown'
            return self.load_intrinsic_func(alias_f, fn_name,
                                            func_exc[fn_name], context, line)

        fn_name_node = fn_name.replace('::', ':')
        alias_fn_name = create_alias(fn_name_node)
        alias_fn_node = create_alias(f'fn_{alias_f}_{alias_fn_name}', True)
        alias_rel = create_alias(f'rel_{alias_f}_{alias_fn_name}', True)
        # add node to context
        context.update([alias_fn_node, alias_f])
        contexts_str = ', '.join(context)

        # create relationship with condition
        statement = (f"CREATE ({alias_f})-"
                     f"[{alias_rel}:EXECUTE_FN]->"
                     f"({alias_fn_node}:{fn_name_node})\n"
                     f"SET {alias_rel}.line = ${alias_rel}_line\n"
                     f"WITH {contexts_str}\n")
        try:
            line = func_exc[f'{fn_name}.line']
        except KeyError:
            line = 'unknown'
        self.statement_params[f'{alias_rel}_line'] = line
        # add function parameters
        for param in func_exc[fn_name]:
            if not isinstance(param, (OrderedDict, dict, list, CustomDict)):
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

    def load_intrinsic_func(self,
                            resource_alias: str,
                            func_name,
                            attrs,
                            contexts: set = None,
                            line='unknown'):
        """
        Create a statement to load clodformation intrinsic functions.

        :param resource_alias: Resource that is related to the function.
        :param func_name: Name of intrinsic function.
        :param attrs: Attributes of function.
        """
        statement = ""
        if func_name == 'Fn::Base64':
            alias_fn, statement_fn = self._fn_base64(attrs)
            statement = (
                f"{statement_fn}"
                f'CREATE ({resource_alias})-[:EXECUTE_FN]->({alias_fn})\n')
        elif func_name == 'Ref':
            statement = self._fn_reference(
                resource_alias, attrs, contexts, line)
        return statement

    def _fn_base64(self, attrs, contexts: set = None):
        """Load intrinsic function Fn::Base64."""
        contexts = contexts or set({})
        alias_fn = create_alias("fn_base_base64", True)
        statement = f"CREATE ({alias_fn}: Fn:Base64)\n"
        if isinstance(attrs, (str)):
            statement += (f"SET {alias_fn}.param = ${alias_fn}_value\n")
            self.statement_params[f'{alias_fn}_value'] = attrs
        elif isinstance(attrs, (OrderedDict, list)):
            for key, _ in attrs.items():
                if key in INTRINSIC_FUNCS:
                    try:
                        line = attrs[f'{key}.line']
                    except KeyError:
                        line = 'unknown'
                    statement += self.load_intrinsic_func(
                        alias_fn, key,
                        attrs[key], contexts, line)
        return (alias_fn, statement)

    def _fn_reference(self,
                      resource_id: str,
                      logical_id: str,
                      contexts: set = None,
                      line='unknown'):
        """Loaf intrinsic function Ref."""
        contexts.add(f'ref_{resource_id}_{logical_id}')
        contexts_str = ', '.join(contexts)
        statement = (f"MATCH (ref_{resource_id}_{logical_id}: Parameter)\n"
                     f"WHERE ref_{resource_id}_{logical_id}.name = "
                     f"$ref_{resource_id}_{logical_id}_name\n"
                     f"WITH {contexts_str}\n"
                     f"CREATE ({resource_id})-"
                     f"[rel_{resource_id}_{logical_id}:REFERENCE_TO]->"
                     f"(ref_{resource_id}_{logical_id})\n"
                     f"SET rel_{resource_id}_{logical_id}.line = "
                     f"$rel_{resource_id}_{logical_id}_line\n")

        self.statement_params[f'rel_{resource_id}_{logical_id}_line'] = line
        self.statement_params[
            f'ref_{resource_id}_{logical_id}_name'] = logical_id
        return statement
