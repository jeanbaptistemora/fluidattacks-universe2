# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  lintPython = {
    modules = {
      melts = {
        searchPaths.source = [
          outputs."/melts/config/development"
          outputs."/melts/config/runtime"
        ];
        python = "3.8";
        src = "/melts/toolbox";
      };
      meltsTest = {
        searchPaths.source = [
          outputs."/melts/config/development"
          outputs."/melts/config/runtime"
        ];
        python = "3.8";
        src = "/melts/test/src";
      };
    };
  };
}
