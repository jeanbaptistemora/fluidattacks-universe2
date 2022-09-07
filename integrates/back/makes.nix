# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  imports = [
    ./dev/makes.nix
    ./lint/makes.nix
  ];
  securePythonWithBandit = {
    integratesBack = {
      python = "3.9";
      target = "/integrates/back/src";
    };
  };
}
