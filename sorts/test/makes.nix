# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  testPython = {
    sorts = {
      python = "3.8";
      searchPaths = {
        source = [
          outputs."/sorts/config/development"
          outputs."/sorts/config/runtime"
        ];
      };
      src = "/sorts/test";
    };
  };
}
