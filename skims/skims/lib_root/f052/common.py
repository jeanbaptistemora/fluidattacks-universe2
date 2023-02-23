from collections.abc import (
    Iterable,
    Set,
)
from itertools import (
    chain,
)
from lib_root.utilities.javascript import (
    get_default_alias,
    get_named_alias,
    get_namespace_alias,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)


def split_function_name(f_names: str) -> tuple[str, str]:
    name_l = f_names.lower().split(".")
    if len(name_l) < 2:
        return "", name_l[-1]
    return name_l[-2], name_l[-1]


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def is_insecure_encrypt(
    graph: Graph, al_id: NId, algo: str, method: MethodsEnum
) -> bool:
    if algo in {"des", "rc4"}:
        return True
    if (
        algo in {"aes", "rsa"}
        and (args := g.adj_ast(graph, al_id))
        and len(args) > 2
    ):
        return get_eval_danger(graph, args[-1], method)
    return False


def get_eval_triggers(
    graph: Graph, n_id: NId, rules: Set[str], method: MethodsEnum
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger and evaluation.triggers == rules:
            return True
    return False


def insecure_create_cipher(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    ciphers_methods = {
        "createdecipher",
        "createcipher",
        "createdecipheriv",
        "createcipheriv",
    }
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        f_name = graph.nodes[n_id]["expression"]
        _, crypt = split_function_name(f_name)
        if (
            crypt in ciphers_methods
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args := g.adj_ast(graph, al_id))
            and len(args) > 0
            and get_eval_danger(graph, args[0], method)
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes


def insecure_hash(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_methods = complete_attrs_on_set({"crypto.createHash"})

    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        if (
            graph.nodes[n_id]["expression"] in danger_methods
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (test_node := g.match_ast(graph, al_id).get("__0__"))
            and get_eval_danger(graph, test_node, method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_encrypt(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    crypto_methods = {"encrypt", "decrypt"}

    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        f_name = graph.nodes[n_id]["expression"]
        algo, crypt = split_function_name(f_name)
        if (
            crypt in crypto_methods
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and is_insecure_encrypt(graph, al_id, algo, method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_ecdh_key(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_f = {"createecdh"}

    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        f_name = graph.nodes[n_id]["expression"]
        _, key = split_function_name(f_name)
        if (
            key in danger_f
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args := g.adj_ast(graph, al_id))
            and len(args) > 0
            and get_eval_danger(graph, args[0], method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_rsa_keypair(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_f = {"generatekeypair"}
    rules = {"rsa", "unsafemodulus"}

    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        f_name = graph.nodes[n_id]["expression"]
        _, key = split_function_name(f_name)
        if (
            key in danger_f
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args := g.adj_ast(graph, al_id))
            and len(args) > 1
            and get_eval_triggers(graph, al_id, rules, method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_ec_keypair(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_f = {"generatekeypair"}
    rules = {"ec", "unsafecurve"}

    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        f_name = graph.nodes[n_id]["expression"]
        _, key = split_function_name(f_name)
        if (
            key in danger_f
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args := g.adj_ast(graph, al_id))
            and len(args) > 1
            and get_eval_triggers(graph, al_id, rules, method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_hash_library(graph: Graph) -> list[NId]:
    vuln_nodes: list[NId] = []
    if dangerous_name := get_default_alias(graph, "js-sha1"):
        for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
            method_expression = graph.nodes[n_id]["expression"]
            if method_expression.split(".")[0] == dangerous_name:
                vuln_nodes.append(n_id)
    return vuln_nodes


def get_danger_n_id(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> NId | None:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation:
            if evaluation.danger:
                return n_id
            if vuln_n_id := next(iter(evaluation.triggers), None):
                return vuln_n_id
    return None


def jwt_insecure_sign(graph: Graph, method: MethodsEnum) -> list[NId]:
    nodes = graph.nodes
    vuln_nodes: list[NId] = []
    if imported_name := get_default_alias(graph, "jsonwebtoken"):
        for n_id in g.matching_nodes(
            graph,
            label_type="MethodInvocation",
            expression=f"{imported_name}.sign",
        ):
            method_args_n_ids = g.adj_ast(
                graph, nodes[n_id].get("arguments_id"), 1
            )
            if len(method_args_n_ids) < 3 or nodes[method_args_n_ids[2]].get(
                "label_type"
            ) not in {"Object", "SymbolLookup"}:
                vuln_nodes.append(n_id)
                continue

            if vuln_node := get_danger_n_id(
                graph, method_args_n_ids[2], method
            ):
                vuln_nodes.append(vuln_node)
    return vuln_nodes


def jwt_insec_sign_async(graph: Graph, method: MethodsEnum) -> list[NId]:
    def match_predicate(node: dict[str, str]) -> bool:
        return bool(
            node.get("label_type") == "MethodInvocation"
            and (n_exp := node.get("expression"))
            and (
                (n_exp.startswith(f"new{imported_name}"))
                or (n_exp.endswith("setProtectedHeader"))
            )
        )

    nodes = graph.nodes
    vuln_nodes: list[NId] = []
    imported_name = get_default_alias(graph, "jose") or get_namespace_alias(
        graph, "jose"
    )

    for n_id in g.filter_nodes(graph, nodes, match_predicate):
        if (
            (args_n_id := nodes[n_id].get("arguments_id"))
            and (susp_n_id := next(iter(g.adj_ast(graph, args_n_id)), None))
            and get_eval_danger(graph, susp_n_id, method)
        ):
            vuln_nodes.append(susp_n_id)
    return vuln_nodes


def get_insec_auth_default_import(graph: Graph) -> tuple[NId, ...]:
    def match_predicate(node: dict[str, str]) -> bool:
        if (
            (imported_name := get_default_alias(graph, "crypto-js"))
            or (imported_name := get_namespace_alias(graph, "crypto-js"))
        ) and (node.get("label_type") == "MethodInvocation"):
            danger_methods: Set = {
                f"{imported_name}.HmacSHA1",
                f"{imported_name}.HmacSHA256",
            }
            return node.get("expression") in danger_methods
        return False

    return g.filter_nodes(graph, graph.nodes, match_predicate)


def get_insec_auth_direct_import(graph: Graph) -> tuple[NId, ...]:
    def match_predicate(node: dict[str, str]) -> bool:
        import_sha1 = get_default_alias(graph, "crypto-js/hmac-sha1")
        import_sha256 = get_default_alias(graph, "crypto-js/hmac-sha256")
        if (import_sha1 or import_sha256) and (
            node.get("label_type") == "MethodInvocation"
        ):
            return node.get("expression") in {import_sha1, import_sha256}
        return False

    return g.filter_nodes(graph, graph.nodes, match_predicate)


def get_first_arg_eval(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> NId | None:
    if (
        (args_n_id := graph.nodes[n_id].get("arguments_id"))
        and (first_arg_n_id := next(iter(g.adj_ast(graph, args_n_id)), None))
        and get_eval_danger(graph, first_arg_n_id, method)
    ):
        return first_arg_n_id
    return None


def get_insec_auth_crypto_lib_named(
    graph: Graph, method: MethodsEnum
) -> list[NId]:
    def match_predicate(node: dict[str, str]) -> bool:
        return bool(
            (imported_name := get_named_alias(graph, "crypto", "createHmac"))
            and (node.get("label_type") == "MethodInvocation")
            and (node.get("expression") == imported_name)
        )

    vuln_nodes: list[NId] = []
    nodes = graph.nodes

    for n_id in g.filter_nodes(graph, nodes, match_predicate):
        if vuln_n_id := get_first_arg_eval(graph, n_id, method):
            vuln_nodes.append(vuln_n_id)
    return vuln_nodes


def get_insec_auth_crypto_lib(graph: Graph, method: MethodsEnum) -> list[NId]:
    def match_predicate(node: dict[str, str]) -> bool:
        return bool(
            (
                (imported_name := get_default_alias(graph, "crypto"))
                or (imported_name := get_namespace_alias(graph, "crypto"))
            )
            and (node.get("label_type") == "MethodInvocation")
            and (node.get("expression") == f"{imported_name}.createHmac")
        )

    vuln_nodes: list[NId] = []
    nodes = graph.nodes

    for n_id in g.filter_nodes(graph, nodes, match_predicate):
        if vuln_n_id := get_first_arg_eval(graph, n_id, method):
            vuln_nodes.append(vuln_n_id)
    return vuln_nodes


def insec_msg_auth_mechanism(
    graph: Graph, method: MethodsEnum
) -> Iterable[NId]:
    return chain(
        get_insec_auth_default_import(graph),
        get_insec_auth_direct_import(graph),
        get_insec_auth_crypto_lib(graph, method),
        get_insec_auth_crypto_lib_named(graph, method),
    )
