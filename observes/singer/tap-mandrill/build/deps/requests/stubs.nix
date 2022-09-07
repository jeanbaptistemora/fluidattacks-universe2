# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  python_pkgs,
}:
python_pkgs.types-requests.overridePythonAttrs (
  old: rec {
    version = "2.28.9";
    format = "setuptools";
    src = lib.fetchPypi {
      inherit version;
      pname = old.pname;
      sha256 = "/q9YG9WASXpH/oRdUG+juRtITPcG/yd3TodlmDfemWI=";
    };
  }
)
