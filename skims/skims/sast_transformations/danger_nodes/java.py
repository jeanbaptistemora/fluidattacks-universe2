from model import (
    core_model,
    graph_model,
)
from sast_transformations.danger_nodes.utils import (
    mark_function_arg,
    mark_methods_input,
    mark_methods_sink,
    mark_obj_inst_input,
    mark_obj_inst_sink,
)
from utils.string import (
    build_attr_paths,
)


def mark_inputs(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum

    for finding in (
        findings.F112,
        findings.F004,
        findings.F008,
        findings.F021,
        findings.F042,
        findings.F063,
        findings.F089,
        findings.F107,
    ):
        danger_args = {
            *build_attr_paths(
                "javax",
                "servlet",
                "http",
                "HttpServletRequest",
            ),
            *build_attr_paths(
                "org",
                "springframework",
                "web",
                "bind",
                "annotation",
                "RequestParam",
            ),
        }
        mark_function_arg(finding, graph, syntax, danger_args)

    mark_methods_input(
        findings.F052,
        graph,
        syntax,
        {
            "java.security.MessageDigest.getInstance",
        },
    )
    mark_methods_input(
        findings.F034,
        graph,
        syntax,
        {
            "java.lang.Math.random",
        },
    )
    mark_obj_inst_input(
        findings.F052,
        graph,
        syntax,
        {
            *build_attr_paths("java", "util", "Properties"),
        },
    )
    mark_obj_inst_input(
        findings.F034,
        graph,
        syntax,
        {
            *build_attr_paths("java", "util", "Random"),
        },
    )


def mark_sinks(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum

    mark_methods_sink(
        findings.F112,
        graph,
        syntax,
        {
            "addBatch",
            "batchUpdate",
            "execute",
            "executeBatch",
            "executeLargeBatch",
            "executeLargeUpdate",
            "executeQuery",
            "executeUpdate",
            "query",
            "queryForInt",
            "queryForList",
            "queryForLong",
            "queryForMap",
            "queryForObject",
            "queryForRowSet",
        },
    )
    mark_methods_sink(
        findings.F004,
        graph,
        syntax,
        {
            "command",
            "exec",
            "start",
        },
    )
    mark_methods_sink(
        findings.F008,
        graph,
        syntax,
        {
            "format",
            "getWriter.format",
            "getWriter.print",
            "getWriter.printf",
            "getWriter.println",
            "getWriter.write",
        },
    )
    mark_methods_sink(
        findings.F021,
        graph,
        syntax,
        {
            "compile",
            "evaluate",
        },
    )
    mark_methods_sink(
        findings.F034,
        graph,
        syntax,
        {
            "getSession.setAttribute",
            "addCookie",
        },
    )
    mark_methods_sink(
        findings.F042,
        graph,
        syntax,
        {
            "addCookie",
            "evaluate",
        },
    )
    mark_methods_sink(
        findings.F052,
        graph,
        syntax,
        {
            "java.security.MessageDigest.getInstance",
        },
    )
    mark_methods_sink(
        findings.F063,
        graph,
        syntax,
        {
            "java.nio.file.Files.newInputStream",
            "java.nio.file.Paths.get",
        },
    )
    mark_methods_sink(
        findings.F089,
        graph,
        syntax,
        {
            "putValue",
            "setAttribute",
        },
    )
    mark_methods_sink(
        findings.F107,
        graph,
        syntax,
        {
            "search",
        },
    )
    mark_obj_inst_sink(
        findings.F004,
        graph,
        syntax,
        {
            *build_attr_paths("java", "lang", "ProcessBuilder"),
        },
    )
    mark_obj_inst_sink(
        findings.F063,
        graph,
        syntax,
        {
            *build_attr_paths("java", "io", "File"),
            *build_attr_paths("java", "io", "FileInputStream"),
            *build_attr_paths("java", "io", "FileOutputStream"),
        },
    )
