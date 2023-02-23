from symbolic_eval.types import (
    SymbolicEvalArgs,
)

HTTP_INPUTS: set[str] = {
    "Request.Params",
    "Request.Querystring",
    "Request.Form",
    "Request.Cookies",
    "Request.ServerVariables",
}


JS_TS_HTTP_INPUTS: set[str] = {
    "req.body",
    "req.params",
    "req.query",
}


PYTHON_INPUTS: set[str] = {
    "request.GET.get",
    "request.args",
    "request.files",
}


INSECURE_ALGOS = {
    "none",
    "blowfish",
    "bf",
    "des",
    "desede",
    "rc2",
    "rc4",
    "rsa",
}

INSECURE_MODES = {"cbc", "ecb", "ofb"}

INSECURE_HASHES = {"md2", "md4", "md5", "sha1", "sha-1"}


def check_http_inputs(args: SymbolicEvalArgs) -> bool:
    ma_attr = args.graph.nodes[args.n_id]
    member_access = f'{ma_attr["expression"]}.{ma_attr["member"]}'
    return member_access in HTTP_INPUTS


def check_js_ts_http_inputs(args: SymbolicEvalArgs) -> bool:
    n_attrs = args.graph.nodes[args.n_id]
    member_access = f'{n_attrs["member"]}.{n_attrs["expression"]}'
    return member_access in JS_TS_HTTP_INPUTS


def check_python_inputs(args: SymbolicEvalArgs) -> bool:
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["label_type"] != "MemberAccess":
        return False
    member_access = f'{n_attrs["expression"]}.{n_attrs["member"]}'
    return member_access in PYTHON_INPUTS
