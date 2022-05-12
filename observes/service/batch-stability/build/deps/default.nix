{
  lib,
  python_pkgs,
}: let
  pkgs =
    python_pkgs
    // {
      typing-extensions = lib.buildPythonPackage rec {
        pname = "typing_extensions";
        format = "pyproject";
        version = "4.2.0";
        src = lib.fetchPypi {
          inherit pname version;
          sha256 = "8cJGVaDaDRtn8H4XpeayoQWJTmgkuSCWN4uzZo7wI3Y=";
        };
        nativeBuildInputs = [python_pkgs.flit-core];
      };
    };
  _typing_ext_override = x:
    if x.pname == "typing-extensions"
    then pkgs.typing-extensions
    else x;
in
  pkgs
  // {
    import-linter = import ./import-linter {
      inherit lib;
      click = pkgs.click;
      networkx = pkgs.networkx;
    };
    mypy = pkgs.mypy.overridePythonAttrs (
      old: {
        propagatedBuildInputs = map _typing_ext_override old.propagatedBuildInputs;
      }
    );
    mypy-boto3-batch = import ./boto3/batch-stubs.nix lib pkgs;
    types-boto3 = import ./boto3/stubs.nix lib pkgs;
    types-click = import ./click/stubs.nix lib;
  }
