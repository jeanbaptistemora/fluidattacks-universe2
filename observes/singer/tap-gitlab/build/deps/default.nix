{
  lib,
  local_pkgs,
  pkgs,
  python_version,
}: let
  _python_pkgs = pkgs."${python_version}Packages";
  aioextensions = _python_pkgs.aioextensions.overridePythonAttrs (
    old: rec {
      version = "20.11.1621472";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "q/sqJ1kPILBICBkubJxfkymGVsATVGhQxFBbUHCozII=";
      };
    }
  );
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
  typing_ext_override = let
    override = x:
      if x ? overridePythonAttrs && (x.pname == "typing-extensions" || x.pname == "typing_extensions")
      then python_pkgs.typing-extensions
      else typing_ext_override x;
  in
    pkg:
      if pkg ? overridePythonAttrs
      then
        pkg.overridePythonAttrs (
          old: {
            nativeBuildInputs = map override (old.nativeBuildInputs or []);
            propagatedBuildInputs = map override (old.propagatedBuildInputs or []);
          }
        )
      else pkg;
in
  python_pkgs
  // {
    inherit aioextensions;
    aiohttp = typing_ext_override python_pkgs.aiohttp;
    asgiref = typing_ext_override python_pkgs.asgiref;
    import-linter = import ./import-linter {
      inherit lib python_pkgs;
    };
    legacy-paginator = typing_ext_override local_pkgs.legacy-paginator."${python_version}".pkg;
    legacy-postgres-client = typing_ext_override local_pkgs.legacy-postgres-client."${python_version}".pkg;
    legacy-singer-io = typing_ext_override local_pkgs.legacy-singer-io."${python_version}".pkg;
    mypy = typing_ext_override python_pkgs.mypy;
    mypy-boto3-s3 = import ./boto3/s3-stubs.nix lib python_pkgs;
    types-boto3 = import ./boto3/stubs.nix lib python_pkgs;
    types-cachetools = import ./cachetools/stubs.nix lib;
    types-click = import ./click/stubs.nix lib;
    types-python-dateutil = import ./dateutil/stubs.nix lib;
  }
