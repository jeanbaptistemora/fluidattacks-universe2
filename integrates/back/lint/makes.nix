# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  outputs,
  projectPath,
  ...
}: {
  lintPython = {
    dirsOfModules = {
      integrates = {
        searchPaths = {
          pythonMypy = [
            (projectPath "/integrates/back/src")
          ];
          source = [
            outputs."/integrates/back/env/pypi/runtime"
            outputs."/integrates/back/env/pypi/unit-tests"
          ];
        };
        python = "3.9";
        src = "/integrates/back/src";
      };
      integratesBackChartsGenerators = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/charts/pypi"
        ];
        python = "3.9";
        src = "/integrates/charts/generators";
      };
    };
    imports = {
      integrates = {
        config = "/integrates/back/setup.imports.cfg";
        src = "/integrates/back/src";
      };
    };
    modules = {
      integratesBackDeployPermissionsMatrix = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
        ];
        python = "3.9";
        src = "/integrates/back/deploy/permissions_matrix";
      };
      integratesBackMigrations = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
        ];
        python = "3.9";
        src = "/integrates/back/migrations";
      };
      integratesBackTest = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/unit-tests"
          outputs."/integrates/back/env/pypi/runtime"
        ];
        python = "3.9";
        src = "/integrates/back/test";
      };
      integratesBackTestE2e = {
        searchPaths.source = [
          outputs."/integrates/web/e2e/pypi"
        ];
        python = "3.9";
        src = "/integrates/back/test/e2e/src";
      };
    };
  };
}
