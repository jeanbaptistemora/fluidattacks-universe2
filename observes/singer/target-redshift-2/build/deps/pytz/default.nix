# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  python_pkgs,
}:
python_pkgs.pytz.overridePythonAttrs (
  old: rec {
    version = "2021.3";
    src = lib.fetchPypi {
      inherit version;
      pname = old.pname;
      sha256 = "rK0tiyChrwfU5MnS6ShcXtkQQ1QGLydfP82I3O9PEyY=";
    };
  }
)
