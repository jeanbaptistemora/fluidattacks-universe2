# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  python_pkgs,
}:
python_pkgs.requests.overridePythonAttrs (
  old: rec {
    version = "2.28.1";
    src = lib.fetchPypi {
      inherit version;
      pname = old.pname;
      sha256 = "fFWZsQL+3apmHIJsVqtP7ii/0X9avKHrvj5/GdfJeYM=";
    };
  }
)
