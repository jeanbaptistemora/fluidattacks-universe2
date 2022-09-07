# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  python_pkgs,
}:
python_pkgs.click.overridePythonAttrs (
  old: rec {
    version = "7.1.2";
    src = lib.fetchPypi {
      inherit version;
      pname = old.pname;
      sha256 = "0rUlXHxjSbwb0eWeCM0SrLvWPOZJ8liHVXg6qU37axo=";
    };
  }
)
