from model import (
    core_model,
    graph_model,
)
from sast_symbolic_evaluation.cases.method_invocation.go import (
    attempt_go_parse_float,
)
from sast_symbolic_evaluation.cases.method_invocation.java import (
    attempt_java_looked_up_class,
    attempt_java_security_msgdigest,
    attempt_java_util_properties_methods,
    list_add as java_list_add,
    list_remove as java_list_remove,
)
from sast_symbolic_evaluation.cases.method_invocation.javascript import (
    list_concat as javascript_list_concat,
    list_get as javascript_list_get,
    list_pop as javascript_list_pop,
    list_push as javascript_list_push,
    list_shift as javascript_list_shift,
    process as javascript_process,
    process_cookie as javascript_process_cookie,
)
from sast_symbolic_evaluation.lookup import (
    lookup_class,
    lookup_field,
    lookup_method,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    JavaClassInstance,
)
from sast_symbolic_evaluation.utils_generic import (
    complete_attrs_on_dict,
    lookup_var_dcl_by_name,
    lookup_var_state_by_name,
)
from typing import (
    Any,
    Dict,
    Optional,
    Set,
)
from utils.string import (
    complete_attrs_on_set,
    split_on_first_dot,
    split_on_last_dot,
)

BY_ARGS_PROPAGATION: Set[str] = complete_attrs_on_set(
    {
        "java.net.URLDecoder.decode",
        "java.nio.file.Files.newInputStream",
        "java.nio.file.Paths.get",
        "org.apache.commons.codec.binary.Base64.decodeBase64",
        "org.apache.commons.codec.binary.Base64.encodeBase64",
        "org.springframework.jdbc.core.JdbcTemplate.batchUpdate",
        "org.springframework.jdbc.core.JdbcTemplate.execute",
        "org.springframework.jdbc.core.JdbcTemplate.query",
        "org.springframework.jdbc.core.JdbcTemplate.queryForInt",
        "org.springframework.jdbc.core.JdbcTemplate.queryForList",
        "org.springframework.jdbc.core.JdbcTemplate.queryForLong",
        "org.springframework.jdbc.core.JdbcTemplate.queryForMap",
        "org.springframework.jdbc.core.JdbcTemplate.queryForObject",
        "org.springframework.jdbc.core.JdbcTemplate.queryForRowSet",
        "org.owasp.esapi.ESAPI.encoder.encodeForBase64",
        "org.owasp.esapi.ESAPI.encoder.decodeForBase64",
        "Double.toString",
        "Float.toString",
        "Integer.toString",
        "Long.toString",
        "System.Diagnostics.Process.Start",
        "System.IO.File.Copy",
        "System.IO.File.Create",
        "System.IO.File.Delete",
        "System.IO.File.Exists",
        "System.IO.File.Move",
        "System.IO.File.Open",
        "System.IO.File.Replace",
        "System.IO.Path.Combine",
        "System.Xml.XPath.XPathExpression.Compile",
        "Encoding.UTF8.GetBytes",
        # javascript
        "child_process.exec",
        "child_process.execSync",
        "decodeURI",
        "encodeURIComponent",
        "Object.values",
        "fs.readFile",
        "fs.readFileSync",
        "fs.unlink",
        "fs.unlinkSync",
        "path.join",
        "path.resolve",
        "fs.writeFile",
        "fs.writeFileSync",
        "fs.readdir",
        "fs.readdirSync",
        "fs.exist",
        "fs.existSync",
        "fs.rmdir",
        "fs.rmdir",
        "fs.rmdirSync",
        "fs.stat",
        "fs.statSync",
        "fs.appendFile",
        "fs.appendFileSync",
        "fs.chown",
        "fs.chownSync",
        "fs.chmod",
        "fs.chmodSync",
        "fs.copyFile",
        "fs.copyFileSync",
        "fs.createReadStream",
        "fs.createWriteStream",
        "fs.exists",
        "fs.existsSync",
    }
)
STATIC_FINDING: Dict[str, Set[str]] = {
    core_model.FindingEnum.F034.name: complete_attrs_on_set(
        {
            "java.lang.Math.random",
            "java.util.Random.nextFloat",
            "java.util.Random.nextInt",
            "java.util.Random.nextLong",
            "java.util.Random.nextBoolean",
            "java.util.Random.nextDouble",
            "java.util.Random.nextGaussian",
        }
    ),
    core_model.FindingEnum.F001.name: complete_attrs_on_set(
        {
            "System.Console.ReadLine",
        }
    ),
    core_model.FindingEnum.F107.name: complete_attrs_on_set(
        {
            "Environment.GetEnvironmentVariable",
        }
    ),
    core_model.FindingEnum.F004.name: complete_attrs_on_set(
        {
            "Environment.GetEnvironmentVariable",
        }
    ),
    core_model.FindingEnum.F021.name: complete_attrs_on_set(
        {
            "Environment.GetEnvironmentVariable",
        }
    ),
    core_model.FindingEnum.F063.name: complete_attrs_on_set(
        {
            "Environment.GetEnvironmentVariable",
        }
    ),
}
STATIC_SIDE_EFFECTS: Dict[str, Set[str]] = {
    core_model.FindingEnum.F034.name: complete_attrs_on_set(
        {
            "java.util.Random.nextBytes",
        }
    ),
}
BY_OBJ_NO_TYPE_ARGS_PROPAG: Dict[str, Set[str]] = {
    core_model.FindingEnum.F034.name: complete_attrs_on_set(
        {
            "getSession.setAttribute",
            "toString.substring",
            "addCookie",
        }
    ),
    core_model.FindingEnum.F021.name: complete_attrs_on_set(
        {
            "Split",
        }
    ),
    core_model.FindingEnum.F089.name: complete_attrs_on_set(
        {
            "org.apache.commons.lang.StringEscapeUtils.escapeHtml",
            "org.springframework.web.util.HtmlUtils.htmlEscape",
            "org.owasp.esapi.ESAPI.encoder.encodeForHTML",
        }
    ),
    core_model.FindingEnum.F127.name: complete_attrs_on_set(
        {
            "Exec",
            "ExecContext",
            "Query",
            "QueryContext",
            "QueryRow",
            "QueryRowContext",
        }
    ),
}
BY_OBJ: Dict[str, Set[str]] = complete_attrs_on_dict(
    {
        "java.lang.String": {
            "getBytes",
            "split",
            "substring",
            "toCharArray",
        },
        "string": {
            "Split",
            "Replace",
            "concat",
        },
        "java.lang.StringBuilder": {
            "append",
            "append.toString",
            "toString",
        },
        "java.sql.CallableStatement": {
            "executeQuery",
        },
        "java.sql.PreparedStatement": {
            "execute",
        },
        "org.springframework.jdbc.core.JdbcTemplate": {
            "query",
            "queryForList",
            "queryForMap",
            "queryForObject",
            "queryForRowSet",
            "queryForStream",
        },
        "java.util.Enumeration": {
            "nextElement",
        },
        "java.util.Map": {
            "get",
        },
        "java.util.List": {
            "get",
        },
        "System.Data.SqlClient.SqlCommand": {
            "ExecuteNonQuery",
            "ExecuteReader",
            "ExecuteScalar",
            "ExecuteNonQueryAsync",
            "ExecuteScalarAsync",
            "ExecuteReaderAsync",
        },
        "System.Data.SQLite.SQLite.SQLiteCommand": {
            "ExecuteNonQuery",
            "ExecuteReader",
            "ExecuteScalar",
            "ExecuteNonQueryAsync",
            "ExecuteScalarAsync",
            "ExecuteReaderAsync",
        },
        "System.Data.OracleClient.OracleCommand": {
            "ExecuteNonQuery",
            "ExecuteOracleNonQuery",
            "ExecuteOracleScalar",
            "ExecuteReader",
            "ExecuteScalar",
            "ExecuteNonQueryAsync",
            "ExecuteScalarAsync",
            "ExecuteReaderAsync",
        },
        "MySql.Data.MySqlClient.MySqlCommand": {
            "ExecuteNonQuery",
            "ExecuteReader",
            "ExecuteScalar",
            "ExecuteNonQueryAsync",
            "ExecuteScalarAsync",
            "ExecuteReaderAsync",
        },
        "Npgsql.NpgsqlCommand": {
            "ExecuteNonQuery",
            "ExecuteReader",
            "ExecuteScalar",
            "ExecuteNonQueryAsync",
            "ExecuteScalarAsync",
            "ExecuteReaderAsync",
        },
        "MySql.Data.MySqlClient.MySqlDataReader": {
            "ToString",
        },
        "System.DirectoryServices.DirectorySearcher": {
            "FindOne",
        },
        "System.IO.StreamReader": {
            "ReadLine",
            "ReadToEnd",
        },
        "System.Net.WebClient": {
            "OpenRead",
        },
        "System.Diagnostics.Process": {
            "Start",
        },
    }
)
BY_OBJ_ARGS: Dict[str, Set[str]] = complete_attrs_on_dict(
    {
        "java.sql.Connection": {
            "prepareCall",
            "prepareStatement",
        },
        "java.sql.Statement": {
            "addBatch",
            "execute",
            "executeBatch",
            "executeLargeBatch",
            "executeLargeUpdate",
            "executeQuery",
            "executeUpdate",
        },
        "javax.xml.xpath.XPath": {
            "evaluate",
            "compile",
        },
        "System.Security.Cryptography.AesCryptoServiceProvider": {
            "CreateEncryptor",
        },
        # javascrip
        "child_process": {
            "exec",
            "execSync",
        },
        "string": {
            "concat",
        },
        "fs": {
            "readFile",
            "readFileSync",
            "unlink",
            "unlinkSync",
            "writeFile",
            "writeFileSync",
            "readdir",
            "readdirSync",
            "exist",
            "existSync",
            "rmdir",
            "rmdir",
            "rmdirSync",
            "stat",
            "statSync",
            "appendFile",
            "appendFileSync",
            "chown",
            "chownSync",
            "chmod",
            "chmodSync",
            "copyFile",
            "copyFileSync",
            "createReadStream",
            "createWriteStream",
            "exists",
            "existsSync",
        },
        "path": {
            "join",
        },
    }
)
BY_TYPE: Dict[str, Set[str]] = complete_attrs_on_dict(
    {
        "javax.servlet.http.Cookie": {
            "getName",
            "getValue",
        },
        "javax.servlet.http.HttpServletRequest": {
            "getHeader",
            "getHeaderNames",
            "getHeaders",
            "getParameter",
            "getParameterMap",
            "getParameterNames",
            "getParameterValues",
            "getQueryString",
        },
        "System.Web.HttpRequest": {
            "Params.Get",
        },
        "System.Net.Sockets.TcpClient": {
            "GetStream",
        },
        "System.Net.Sockets.TcpListener": {
            "AcceptTcpClient",
        },
        "System.Data.SqlClient.SqlDataReader": {
            "GetString",
        },
    }
)
BY_TYPE_AND_VALUE_FINDING: Dict[str, Dict[str, Any]] = {
    core_model.FindingEnum.F008.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.HttpServletResponse": {
                "setHeader": {
                    "X-XSS-Protection",
                    "0",
                },
            },
        }
    ),
    core_model.FindingEnum.F042.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.Cookie": {
                "setSecure": {
                    False,
                },
            },
        }
    ),
}
BY_TYPE_ARGS_PROPAGATION: Dict[str, Set[str]] = complete_attrs_on_dict(
    {
        "java.io.PrintWriter": {
            "format",
        },
        "java.util.List": {
            "add",
        },
    }
)
BY_TYPE_ARGS_PROPAG_FINDING: Dict[str, Dict[str, Set[str]]] = {
    core_model.FindingEnum.F042.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.HttpServletResponse": {
                "addCookie",
            },
        }
    ),
    core_model.FindingEnum.F034.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.HttpServletResponse": {
                "addCookie",
            },
            "javax.servlet.http.HttpServletRequest": {
                "getSession.setAttribute",
            },
        }
    ),
    core_model.FindingEnum.F004.name: complete_attrs_on_dict(
        {
            "ProcessBuilder": {
                "command",
            },
            "Runtime": {
                "exec",
            },
        }
    ),
    core_model.FindingEnum.F021.name: complete_attrs_on_dict(
        {
            "System.Xml.XPath.XPathNavigator": {
                "Evaluate",
                "Select",
            },
        }
    ),
    core_model.FindingEnum.F008.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.HttpServletResponse": {
                "getWriter.format",
                "getWriter.print",
                "getWriter.printf",
                "getWriter.println",
                "getWriter.write",
            },
            "System.Web.HttpResponse": {
                "Write",
                "AddHeader",
            },
            "Response": {
                "send",
            },
        }
    ),
    core_model.FindingEnum.F089.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.HttpServletRequest": {
                "getSession.putValue",
                "getSession.setAttribute",
            },
        }
    ),
    core_model.FindingEnum.F107.name: complete_attrs_on_dict(
        {
            "javax.naming.directory.InitialDirContext": {
                "search",
            },
            "javax.naming.directory.DirContext": {
                "search",
            },
        }
    ),
}
BY_TYPE_HANDLER = complete_attrs_on_dict(
    {
        "Response": {
            "cookie": {
                javascript_process_cookie,
            },
        },
    }
)


def evaluate(args: EvaluatorArgs) -> None:
    language = args.shard.metadata.language

    if language == graph_model.GraphShardMetadataLanguage.JAVASCRIPT:
        javascript_process(args)

    if language == graph_model.GraphShardMetadataLanguage.GO:
        evaluate_go(args)

    if language in (
        graph_model.GraphShardMetadataLanguage.JAVA,
        graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
        graph_model.GraphShardMetadataLanguage.CSHARP,
    ):
        evaluate_many(args)


def evaluate_go(args: EvaluatorArgs) -> None:
    # pylint: disable=expression-not-assigned
    (attempt_go_parse_float(args) or attempt_the_old_way(args))


def evaluate_many(args: EvaluatorArgs) -> None:
    # pylint: disable=expression-not-assigned
    (
        attempt_java_util_properties_methods(args)
        or attempt_java_security_msgdigest(args)
        or attempt_the_old_way(args)
        or attempt_java_looked_up_class(args)
    )


def attempt_by_args_propagation_no_type(
    args: EvaluatorArgs,
    method: str,
) -> bool:
    _, method_path = split_on_first_dot(method)

    if method_path in BY_OBJ_NO_TYPE_ARGS_PROPAG.get(
        args.finding.name, {}
    ) and any(dep.meta.danger for dep in args.dependencies):
        args.syntax_step.meta.danger = True
        return True

    return False


def attempt_by_args_propagation(args: EvaluatorArgs, method: str) -> bool:
    method_field, method_name = split_on_last_dot(args.syntax_step.method)
    if field := lookup_field(args, method_field):
        method = f"{field.metadata.var_type}.{method_name}"

    if (method in BY_ARGS_PROPAGATION) and any(
        dep.meta.danger for dep in args.dependencies
    ):
        args.syntax_step.meta.danger = True
        return True

    return False


def attempt_by_obj(args: EvaluatorArgs, method: str) -> bool:
    method_var, method_path = split_on_first_dot(method)

    # pylint: disable=used-before-assignment
    if (
        (method_var_decl := lookup_var_dcl_by_name(args, method_var))
        and (
            method_var_decl.var_type_base
            and method_path in BY_OBJ.get(method_var_decl.var_type_base, {})
        )
        and (method_var_state := lookup_var_state_by_name(args, method_var))
        and (method_var_state.meta.danger)
    ):
        args.syntax_step.meta.danger = True
        return True

    return False


def attempt_by_obj_args(args: EvaluatorArgs, method: str) -> bool:
    method_var, method_path = split_on_first_dot(method)

    # pylint: disable=used-before-assignment
    if (
        (method_var_decl := lookup_var_dcl_by_name(args, method_var))
        and (
            method_var_decl.var_type_base
            and method_path
            in BY_OBJ_ARGS.get(method_var_decl.var_type_base, {})
        )
        and any(dep.meta.danger for dep in args.dependencies)
    ):
        args.syntax_step.meta.danger = True
        return True

    return False


def attempt_by_type_args_propagation(args: EvaluatorArgs, method: str) -> bool:
    # Functions that when called make the parent object vulnerable
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    method_var, method_path = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)

    if args_danger and method_var_decl and method_var_decl.var_type_base:
        if method_path in (
            BY_TYPE_ARGS_PROPAGATION.get(method_var_decl.var_type_base, {})
        ):
            args.syntax_step.meta.danger = True
            method_var_decl.meta.danger = True
            return True

        if method_path in (
            BY_TYPE_ARGS_PROPAG_FINDING.get(args.finding.name, {}).get(
                method_var_decl.var_type_base, {}
            )
        ):
            args.syntax_step.meta.danger = True
            return True

    return False


def attempt_by_type_and_value_finding(
    args: EvaluatorArgs,
    method: str,
) -> bool:
    # function calls with parameters that make the object vulnerable
    method_var, method_path = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)

    if (
        method_var_decl
        and method_var_decl.var_type_base
        and (
            methods := (
                BY_TYPE_AND_VALUE_FINDING.get(args.finding.name, {}).get(
                    method_var_decl.var_type_base
                )
            )
        )
    ):
        parameters = {param.meta.value for param in args.dependencies}
        if parameters.issubset(methods.get(method_path, set())):
            method_var_decl.meta.danger = True
            return True

    return False


def attempt_static(args: EvaluatorArgs, method: str) -> bool:
    if method in STATIC_FINDING.get(args.finding.name, {}):
        args.syntax_step.meta.danger = True
        return True
    return False


def attempt_static_side_effects(args: EvaluatorArgs, method: str) -> bool:
    if method in STATIC_SIDE_EFFECTS.get(args.finding.name, {}):
        for dep in args.dependencies:
            dep.meta.danger = True
        return True
    return False


def attempt_by_type(args: EvaluatorArgs, method: str) -> bool:
    method_var, method_path = split_on_first_dot(method)

    # pylint: disable=used-before-assignment
    if (
        (method_var_decl := lookup_var_dcl_by_name(args, method_var))
        and method_var_decl.var_type_base
        and (method_path in BY_TYPE.get(method_var_decl.var_type_base, {}))
    ):
        args.syntax_step.meta.danger = True
        return True

    if (method_var_decl := lookup_field(args, method_var)) and (
        method_path in BY_TYPE.get(method_var_decl.metadata.var_type, {})
    ):
        args.syntax_step.meta.danger = True
        return True

    return False


def attemp_by_type_handler(args: EvaluatorArgs, method: str) -> bool:
    method_var, method_path = split_on_first_dot(method)

    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    if (
        method_var_decl
        and method_var_decl.var_type_base
        and (
            handlers := BY_TYPE_HANDLER.get(
                method_var_decl.var_type_base, {}
            ).get(method_path)
        )
    ):
        for handler in handlers:
            handler(args)
        return True

    return False


def attempt_the_old_way(args: EvaluatorArgs) -> bool:
    # Analyze if the method itself is untrusted
    method = args.syntax_step.method

    analyze_method_invocation(args, method)
    analyze_method_invocation_values(args)

    return False


def analyze_method_invocation(args: EvaluatorArgs, method: str) -> None:
    # pylint: disable=expression-not-assigned,too-many-boolean-expressions
    (
        attempt_static(args, method)
        or attempt_static_side_effects(args, method)
        or attempt_by_args_propagation_no_type(args, method)
        or attempt_by_type_args_propagation(args, method)
        or attempt_by_obj(args, method)
        or attempt_by_obj_args(args, method)
        or attempt_by_type_and_value_finding(args, method)
        or attempt_by_args_propagation(args, method)
        or attempt_by_type(args, method)
        or analyze_method_invocation_local(args, method)
        or analyze_method_invocation_external(args, method)
        or attemp_by_type_handler(args, method)
    )


def analyze_method_invocation_local(
    args: EvaluatorArgs,
    method: str,
) -> bool:
    method_var, method_path = split_on_first_dot(method)

    if method_var == "this":
        method_name = method_path
    elif not method_path and method_var:
        method_name = method_var
    else:
        return False

    if (_method := lookup_method(args, method_name)) and (
        return_step := args.eval_method(
            args,
            # pylint: disable=used-before-assignment
            _method.metadata.n_id,
            args.dependencies,
            args.graph_db.shards_by_path_f(_method.shard_path),
        )
    ):
        args.syntax_step.meta.danger = return_step.meta.danger
        args.syntax_step.meta.value = return_step.meta.value
        return True

    return False


def analyze_method_invocation_external(
    args: EvaluatorArgs,
    method: str,
) -> bool:
    method_var, method_path = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    method_var_decl_type = None

    if method_var_decl:
        method_var_decl_type = method_var_decl.var_type
    # lookup methods with teh format new Test().some()
    # last argument is teh instance
    elif (
        args.dependencies
        and isinstance(
            args.dependencies[-1],
            graph_model.SyntaxStepObjectInstantiation,
        )
        and lookup_class(
            args,
            args.dependencies[-1].object_type,
        )
    ):
        method_var_decl_type = args.dependencies[-1].object_type

    if method_var_decl_type and (
        _method := lookup_method(
            args,
            method_path,
            method_var_decl_type,
        )
    ):
        if args.shard.path != _method.shard_path and (
            return_step := args.eval_method(
                args,
                _method.metadata.n_id,
                args.dependencies,
                args.graph_db.shards_by_path_f(_method.shard_path),
                method_var_decl.meta.value if method_var_decl else None,
            )
        ):
            args.syntax_step.meta.danger = return_step.meta.danger
            args.syntax_step.meta.value = return_step.meta.value
            return True

    return False


def analyze_method_invocation_values(
    args: EvaluatorArgs,
    method: Optional[str] = None,
) -> None:
    method = method or args.syntax_step.method
    method_var, method_path = split_on_first_dot(method)
    method_var_decl_type = None
    # lookup methods with teh format new Test().some()
    # last argument is teh instance
    if (
        args.dependencies
        and isinstance(
            args.dependencies[-1],
            graph_model.SyntaxStepObjectInstantiation,
        )
        and lookup_class(
            args,
            args.dependencies[-1].object_type,
        )
    ):
        method_var_decl_type = args.dependencies[-1].object_type

    if dcl := lookup_var_state_by_name(args, method_var):
        if isinstance(dcl.meta.value, dict):
            analyze_method_invocation_values_dict(args, dcl, method_path)
        if isinstance(dcl.meta.value, str):
            analyze_method_invocation_values_str(args, dcl, method_path)
        if isinstance(dcl.meta.value, list):
            analyze_method_invocation_values_list(args, dcl, method_path)
    elif _method := lookup_method(args, method) or (
        _method := lookup_method(
            args,
            method_path or method_var,  # can be local function
            method_var_decl_type,
        )
    ):
        class_instance = (
            JavaClassInstance(
                fields={},
                class_name=method_var_decl_type,
            )
            if lookup_class(args, _method.metadata.class_name)
            else None
        )

        if return_step := args.eval_method(
            args,
            _method.metadata.n_id,
            args.dependencies,
            args.graph_db.shards_by_path_f(_method.shard_path),
            class_instance,
        ):
            args.syntax_step.meta.danger = return_step.meta.danger
            args.syntax_step.meta.value = return_step.meta.value
        if class_instance and args.syntax_step.current_instance:
            args.syntax_step.current_instance.fields.update(
                class_instance.fields
            )


def analyze_method_invocation_values_dict(
    args: EvaluatorArgs,
    dcl: graph_model.SyntaxStep,
    method_path: str,
) -> None:
    if method_path == "put":
        value, key = args.dependencies
        dcl.meta.value[key.meta.value] = value
    elif method_path == "get":
        key = args.dependencies[0]
        args.syntax_step.meta.value = dcl.meta.value.get(key.meta.value)
        args.syntax_step.meta.danger = (
            dcl.meta.value[key.meta.value].meta.danger
            if key.meta.value in dcl.meta.value
            else False
        )


def analyze_method_invocation_values_str(
    args: EvaluatorArgs,
    dcl: graph_model.SyntaxStep,
    method_path: str,
) -> None:
    if method_path == "charAt":
        index = int(args.dependencies[0].meta.value)
        args.syntax_step.meta.value = dcl.meta.value[index]


def analyze_method_invocation_values_list(
    args: EvaluatorArgs,
    dcl: graph_model.SyntaxStep,
    method_path: str,
) -> None:
    methods = {
        "add": java_list_add,
        "remove": java_list_remove,
        "get": javascript_list_get,
        "pop": javascript_list_pop,
        "shift": javascript_list_shift,
        "push": javascript_list_push,
        "concat": javascript_list_concat,
    }
    if method := methods.get(method_path):
        method(args, dcl)
