# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  pkgs,
  lib,
  local_pkgs,
  python_version,
}: let
  pythonPkgs = pkgs."${python_version}Packages";
  jsonschema = pythonPkgs.jsonschema.overridePythonAttrs (
    old: rec {
      version = "3.2.0";
      SETUPTOOLS_SCM_PRETEND_VERSION = version;
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "yKhbKNN3zHc35G4tnytPRO48Dh3qxr9G3e/HGH0weXo=";
      };
    }
  );
in
  pythonPkgs
  // {
    inherit jsonschema;
    legacy-purity = local_pkgs.legacy-purity."${python_version}".pkg;
  }
