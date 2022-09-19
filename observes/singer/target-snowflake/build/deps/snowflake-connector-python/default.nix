{
  lib,
  python_pkgs,
}: let
  version = "2.7.12";
  missing_deps = with python_pkgs; [
    filelock
    typing-extensions
  ];
in
  python_pkgs.snowflake-connector-python.overridePythonAttrs (
    old: {
      inherit version;
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "M50YI6aB7fSVRLeAqxLKtsxJIC1oWLcb9Mvah9/C/zU=";
      };
      propagatedBuildInputs = old.propagatedBuildInputs ++ missing_deps;
    }
  )
