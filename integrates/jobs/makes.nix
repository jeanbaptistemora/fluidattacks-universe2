# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  outputs,
  projectPath,
  ...
}: {
  lintPython = {
    modules = {
      integratesJobsCloneRoots = {
        searchPaths = {
          source = [
            outputs."/integrates/jobs/clone_roots/env"
          ];
          pythonMypy = [
            (projectPath "/integrates/jobs/clone_roots/src")
          ];
        };
        python = "3.8";
        src = "/integrates/jobs/clone_roots/src";
      };
    };
  };
}
