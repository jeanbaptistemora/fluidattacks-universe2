{
  lib,
  pkgs,
  python_version,
}: let
  _python_pkgs = pkgs."${python_version}Packages";
  python_pkgs =
    _python_pkgs
    // {
      typing-extensions = lib.buildPythonPackage rec {
        pname = "typing_extensions";
        format = "pyproject";
        version = "4.2.0";
        src = lib.fetchPypi {
          inherit pname version;
          sha256 = "8cJGVaDaDRtn8H4XpeayoQWJTmgkuSCWN4uzZo7wI3Y=";
        };
        nativeBuildInputs = [_python_pkgs.flit-core];
      };
    };
  pkg_override = import ./pkg_override.nix;
  typing_ext_override = pkg_override (x: (x.pname == "typing-extensions" || x.pname == "typing_extensions")) python_pkgs.typing-extensions;
in
  python_pkgs
  // {
    import-linter = import ./import-linter {
      inherit lib python_pkgs;
    };
    mypy = typing_ext_override python_pkgs.mypy;
  }
