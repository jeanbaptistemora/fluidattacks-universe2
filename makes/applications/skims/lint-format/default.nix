{ lintPythonFormat
, ...
}:
lintPythonFormat {
  target = "skims/skims/";
  name = "skims-lint-format";
}
