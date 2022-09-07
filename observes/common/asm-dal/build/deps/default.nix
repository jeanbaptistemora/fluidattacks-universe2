# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  pkgs,
  python_version,
}: let
  _python_pkgs = pkgs."${python_version}Packages";
  fa-purity = typing_ext_override pkgs.fa-purity."${python_version}".pkg;
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
  pkg_override = is_pkg: new_pkg: let
    override = x:
      if x ? overridePythonAttrs && is_pkg x
      then new_pkg
      else pkg_override is_pkg new_pkg x;
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
  typing_ext_override = pkg_override (x: (x.pname == "typing-extensions" || x.pname == "typing_extensions")) python_pkgs.typing-extensions;
in
  python_pkgs
  // {
    inherit fa-purity;
    import-linter = import ./import-linter {
      inherit lib python_pkgs;
    };
    mypy = typing_ext_override python_pkgs.mypy;
    mypy-boto3-dynamodb = import ./boto3/dynamodb-stubs.nix lib python_pkgs;
    types-boto3 = import ./boto3/stubs.nix lib python_pkgs;
    types-click = import ./click/stubs.nix lib;
    utils-logger = pkgs.utils-logger."${python_version}".pkg;
  }
