from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
import utils.graph as g

features_general_entities = (
    "http://xml.org/sax/features/external-general-entities",
    "false",
)

feature_doctype_decl = (
    "http://apache.org/xml/features/disallow-doctype-decl",
    "true",
)

feature_paremeter_entities = (
    "http://xml.org/sax/features/external-parameter-entities",
    "false",
)


methods_inits = {
    "createXMLReader",
    "newInstance",
    "newDocumentBuilder",
    "newSAXParser",
    "DocumentBuilderFactory",
}


def xml_parser(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    graph = args.graph
    if graph.nodes[args.n_id]["expression"] in methods_inits:
        args.evaluation[args.n_id] = True
    if (
        graph.nodes[args.n_id]["expression"] == "setFeature"
        and (arg_list := g.match_ast_d(graph, args.n_id, "ArgumentList"))
        and (arg_features := g.adj_ast(graph, arg_list))
    ):

        arg_features = (
            graph.nodes[arg_features[0]]["value"].strip('"'),
            graph.nodes[arg_features[1]]["value"].strip('"'),
        )
        if arg_features == features_general_entities:
            args.triggers.add("featureEntitisSetted")
        if arg_features == feature_doctype_decl:
            args.triggers.add("featureDoctypeSetted")
        if arg_features == feature_paremeter_entities:
            args.triggers.add("featureParametterSetted")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
