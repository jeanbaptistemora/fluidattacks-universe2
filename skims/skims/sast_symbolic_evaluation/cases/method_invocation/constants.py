from model.core_model import (
    FindingEnum,
)
from sast_symbolic_evaluation.cases.method_invocation.javascript import (
    insecure_crypto_js,
    insecure_key as javascript_insecure_key,
    process_cookie as javascript_process_cookie,
)
from sast_symbolic_evaluation.utils_generic import (
    complete_attrs_on_dict,
)
from typing import (
    Any,
    Dict,
    Set,
)
from utils.string import (
    complete_attrs_on_set,
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
        "crypto.createCipheriv",
        "crypto.createDecipheriv",
    }
)
STATIC_FINDING: Dict[str, Set[str]] = {
    FindingEnum.F034.name: complete_attrs_on_set(
        {
            "java.lang.Math.random",
            "java.util.Random.nextFloat",
            "java.util.Random.nextInt",
            "java.util.Random.nextLong",
            "java.util.Random.nextBoolean",
            "java.util.Random.nextDouble",
            "java.util.Random.nextGaussian",
            # javascrip
            "Math.random",
        }
    ),
    FindingEnum.F001.name: complete_attrs_on_set(
        {
            "System.Console.ReadLine",
        }
    ),
    FindingEnum.F100.name: complete_attrs_on_set(
        {
            "System.Net.WebRequest.Create",
        }
    ),
    FindingEnum.F107.name: complete_attrs_on_set(
        {
            "Environment.GetEnvironmentVariable",
        }
    ),
    FindingEnum.F004.name: complete_attrs_on_set(
        {
            "Environment.GetEnvironmentVariable",
        }
    ),
    FindingEnum.F021.name: complete_attrs_on_set(
        {
            "Environment.GetEnvironmentVariable",
        }
    ),
    FindingEnum.F063.name: complete_attrs_on_set(
        {
            "Environment.GetEnvironmentVariable",
        }
    ),
}
STATIC_SIDE_EFFECTS: Dict[str, Set[str]] = {
    FindingEnum.F034.name: complete_attrs_on_set(
        {
            "java.util.Random.nextBytes",
        }
    ),
}
BY_OBJ_NO_TYPE_ARGS_PROPAG: Dict[str, Set[str]] = {
    FindingEnum.F034.name: complete_attrs_on_set(
        {
            "getSession.setAttribute",
            "toString.substring",
            "addCookie",
            "toString",
        }
    ),
    FindingEnum.F021.name: complete_attrs_on_set(
        {
            "Split",
        }
    ),
    FindingEnum.F089.name: complete_attrs_on_set(
        {
            "org.apache.commons.lang.StringEscapeUtils.escapeHtml",
            "org.springframework.web.util.HtmlUtils.htmlEscape",
            "org.owasp.esapi.ESAPI.encoder.encodeForHTML",
        }
    ),
    FindingEnum.F127.name: complete_attrs_on_set(
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
        "XPath": {"select"},
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
        "xpath": {
            "select",
            "parse",
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
    FindingEnum.F008.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.HttpServletResponse": {
                "setHeader": {
                    "X-XSS-Protection",
                    "0",
                },
            },
        }
    ),
    FindingEnum.F042.name: complete_attrs_on_dict(
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
    FindingEnum.F042.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.HttpServletResponse": {
                "addCookie",
            },
        }
    ),
    FindingEnum.F034.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.HttpServletResponse": {
                "addCookie",
            },
            "javax.servlet.http.HttpServletRequest": {
                "getSession.setAttribute",
            },
            "Response": {
                "cookie",
            },
        }
    ),
    FindingEnum.F004.name: complete_attrs_on_dict(
        {
            "ProcessBuilder": {
                "command",
            },
            "Runtime": {
                "exec",
            },
        }
    ),
    FindingEnum.F021.name: complete_attrs_on_dict(
        {
            "System.Xml.XPath.XPathNavigator": {
                "Evaluate",
                "Select",
            },
        }
    ),
    FindingEnum.F008.name: complete_attrs_on_dict(
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
    FindingEnum.F089.name: complete_attrs_on_dict(
        {
            "javax.servlet.http.HttpServletRequest": {
                "getSession.putValue",
                "getSession.setAttribute",
            },
        }
    ),
    FindingEnum.F107.name: complete_attrs_on_dict(
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
        "crypto": {
            "generateKeyPair": {
                javascript_insecure_key,
            }
        },
        "crypto-js.AES": {
            "encrypt": {
                insecure_crypto_js,
            }
        },
        "crypto-js": {
            "AES.encrypt": {
                insecure_crypto_js,
            },
            "RSA.encrypt": {
                insecure_crypto_js,
            },
        },
        "crypto-js.RSA": {
            "encrypt": {
                insecure_crypto_js,
            }
        },
    }
)
RETURN_TYPES = complete_attrs_on_dict(
    {
        "xpath": {
            "parse": "XPath",
            "useNamespaces": "xpath.XPathSelect",
        },
        "express.Router": {
            "Router": "xpath.Router",
        },
    }
)
