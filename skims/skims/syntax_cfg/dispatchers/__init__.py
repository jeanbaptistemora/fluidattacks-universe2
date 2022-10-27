# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_cfg.dispatchers import (
    connect_to_block,
    connect_to_declarations,
    connect_to_next,
    end_node,
    if_node,
    method_invocation_node,
    multi_path,
    step_by_step,
)
from syntax_cfg.types import (
    Dispatcher,
    Dispatchers,
)

DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "Class",
            "ConstructorDeclaration",
            "DoStatement",
            "ForEachStatement",
            "ForStatement",
            "ElseClause",
            "InterfaceDeclaration",
            "LambdaExpression",
            "MethodDeclaration",
            "Namespace",
            "SwitchStatement",
            "UsingStatement",
            "WhileStatement",
        },
        cfg_builder=connect_to_block.build,
    ),
    Dispatcher(
        applicable_types={
            "ArgumentList",
            "BinaryOperation",
            "DeclarationBlock",
            "File",
            "FileNamespace",
            "PackageDeclaration",
            "TryStatement",
            "SwitchBody",
            "SwitchSection",
            "ClassBody",
        },
        cfg_builder=multi_path.build,
    ),
    Dispatcher(
        applicable_types={
            "ExecutionBlock",
            "ParameterList",
            "StatementBlock",
        },
        cfg_builder=step_by_step.build,
    ),
    Dispatcher(
        applicable_types={
            "If",
        },
        cfg_builder=if_node.build,
    ),
    Dispatcher(
        applicable_types={
            "MethodInvocation",
        },
        cfg_builder=method_invocation_node.build,
    ),
    Dispatcher(
        applicable_types={
            "ArrayInitializer",
            "ArrowExpressionClause",
            "Assignment",
            "Break",
            "BlocklessMethodDeclaration",
            "CatchClause",
            "CatchDeclaration",
            "Continue",
            "Comment",
            "Debugger",
            "ElementAccess",
            "FieldAccess",
            "FieldDeclaration",
            "FinallyClause",
            "FunctionBody",
            "LexicalDeclaration",
            "Literal",
            "MemberAccess",
            "MethodSignature",
            "MissingNode",
            "NewExpression",
            "Object",
            "ObjectCreation",
            "PostfixUnaryExpression",
            "PropertyDeclaration",
            "Resource",
            "SwitchCase",
            "SwitchDefault",
            "SymbolLookup",
            "ThrowStatement",
            "UnaryExpression",
            "UpdateExpression",
            "VariableDeclaration",
            "Yield",
        },
        cfg_builder=connect_to_next.build,
    ),
    Dispatcher(
        applicable_types={
            "Return",
            "Export",
        },
        cfg_builder=connect_to_declarations.build,
    ),
    Dispatcher(
        applicable_types={
            "Import",
        },
        cfg_builder=end_node.build,
    ),
)
