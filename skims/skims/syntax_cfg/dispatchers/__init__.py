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
            "InterfaceDeclaration",
            "MethodDeclaration",
            "Namespace",
        },
        cfg_builder=connect_to_block.build,
    ),
    Dispatcher(
        applicable_types={
            "BinaryOperation",
            "DeclarationBlock",
            "File",
            "ForStatement",
            "PackageDeclaration",
            "TryStatement",
            "SwitchBody",
            "SwitchSection",
            "WhileStatement",
        },
        cfg_builder=multi_path.build,
    ),
    Dispatcher(
        applicable_types={
            "ExecutionBlock",
            "ParameterList",
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
            "CallExpression",
            "CatchClause",
            "CatchDeclaration",
            "ClassBody",
            "Comment",
            "FunctionBody",
            "LexicalDeclaration",
            "Literal",
            "MethodInvocation",
            "PostfixUnaryExpression",
            "SymbolLookup",
            "ThrowStatement",
            "VariableDeclaration",
            "UsingStatement",
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
