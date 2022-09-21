# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  lintPython = {
    modules = {
      integratesJobsCloneRoots = {
        searchPaths = {
          source = [
            outputs."/integrates/jobs/clone_roots/env"
          ];
        };
        python = "3.8";
        src = "/integrates/jobs/clone_roots/src";
      };
      integratesJobsExecuteMachine = {
        searchPaths = {
          source = [
            outputs."/integrates/jobs/execute_machine/env"
          ];
        };
        python = "3.9";
        src = "/integrates/jobs/execute_machine/src";
      };
    };
  };
}
