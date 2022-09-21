# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  lintPython = {
    dirsOfModules = {
      streams = {
        searchPaths = {
          pythonMypy = [
            outputs."/integrates/streams/runtime"
          ];
          source = [
            outputs."/integrates/streams/runtime"
          ];
        };
        python = "3.9";
        src = "/integrates/streams/src";
      };
    };
  };
}
