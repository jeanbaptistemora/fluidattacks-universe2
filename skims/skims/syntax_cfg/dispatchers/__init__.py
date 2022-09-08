# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_cfg.dispatchers import (
    connect_to_block,
    connect_to_next,
    end_node,
    if_node,
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
            "InterfaceDeclaration",
            "MethodDeclaration",
            "Namespace",
        },
        cfg_builder=connect_to_block.build,
    ),
    Dispatcher(
        applicable_types={
            "ArgumentList",
            "BinaryOperation",
            "CallExpression",
            "DeclarationBlock",
            "File",
            "ForStatement",
            "EnhancedForStatement",
            "PackageDeclaration",
            "TryStatement",
            "SwitchBody",
            "SwitchSection",
            "WhileStatement",
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
            "ArrowExpressionClause",
            "Assignment",
            "Break",
            "BlocklessMethodDeclaration",
            "CatchClause",
            "CatchDeclaration",
            "Continue",
            "Comment",
            "ElseClause",
            "Export",
            "FieldAccess",
            "FieldDeclaration",
            "FinallyClause",
            "FunctionBody",
            "LexicalDeclaration",
            "Literal",
            "MemberAccess",
            "MethodInvocation",
            "Object",
            "ObjectCreation",
            "PostfixUnaryExpression",
            "Resource",
            "SwitchCase",
            "SwitchDefault",
            "SwitchExpression",
            "SymbolLookup",
            "ThrowStatement",
            "UnaryExpression",
            "UpdateExpression",
            "VariableDeclaration",
            "UsingStatement",
            "Yield",
        },
        cfg_builder=connect_to_next.build,
    ),
    Dispatcher(
        applicable_types={
            "Import",
            "Return",
        },
        cfg_builder=end_node.build,
    ),
)
