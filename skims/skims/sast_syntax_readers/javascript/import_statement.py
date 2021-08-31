from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    module_name = args.graph.nodes[node_attrs["label_field_source"]][
        "label_text"
    ]

    match = g.match_ast(args.graph, args.n_id, "import_clause")
    import_clause = match["import_clause"]
    if not import_clause:
        return

    match = g.match_ast(
        args.graph,
        import_clause,
        "namespace_import",
        "named_imports",
        "identifier",
    )
    if namespace_import := match["namespace_import"]:
        alias_id = g.adj(args.graph, namespace_import)[2]
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var_type=module_name,
            var=args.graph.nodes[alias_id]["label_text"],
        )
    if named_imports := match["named_imports"]:
        match_import = g.match_ast_group(
            args.graph, named_imports, "import_specifier"
        )
        for import_id in match_import["import_specifier"]:
            import_attrs = args.graph.nodes[import_id]
            export_name = args.graph.nodes[import_attrs["label_field_name"]][
                "label_text"
            ]
            if alias_id := import_attrs.get("label_field_alias"):
                var_name = args.graph.nodes[alias_id]["label_text"]
            else:
                var_name = export_name
            yield SyntaxStepDeclaration(
                meta=SyntaxStepMeta.default(args.n_id),
                var_type=f"{module_name}.{export_name}",
                var=var_name,
            )
    if identifier_id := match["identifier"]:
        var_name = args.graph.nodes[identifier_id]["label_text"]
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var_type=f"{module_name}.{var_name}",
            var=var_name,
        )
