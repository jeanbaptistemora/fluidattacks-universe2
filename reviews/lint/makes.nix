# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  lintPython = {
    dirsOfModules = {
      reviews = {
        searchPaths.source = [
          outputs."/reviews/runtime"
        ];
        python = "3.9";
        src = "/reviews/src";
      };
    };
  };
}
