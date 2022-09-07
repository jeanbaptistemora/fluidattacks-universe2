# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  pythonPkgs,
}:
pythonPkgs
// {
  returns = import ./returns {
    inherit lib pythonPkgs;
  };
  types-psycopg2 = import ./psycopg2/stubs.nix lib;
}
