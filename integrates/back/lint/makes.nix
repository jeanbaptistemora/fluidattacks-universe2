{outputs, ...}: {
  lintPython = {
    dirsOfModules = {
      integrates = {
        searchPaths = {
          source = [
            outputs."/integrates/back/env/pypi/runtime"
            outputs."/integrates/back/env/pypi/unit-tests"
            outputs."/integrates/back/env/pypi/type-stubs"
          ];
        };
        python = "3.9";
        src = "/integrates/back/src";
      };
      integratesBackChartsGenerators = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/charts/pypi"
          outputs."/integrates/back/env/pypi/type-stubs"
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
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.9";
        src = "/integrates/back/deploy/permissions_matrix";
      };
      integratesBackMigrations = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.9";
        src = "/integrates/back/migrations";
      };
      integratesBackTest = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/unit-tests"
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.9";
        src = "/integrates/back/test";
      };
      integratesBackTestE2e = {
        searchPaths.source = [
          outputs."/integrates/web/e2e/pypi"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.9";
        src = "/integrates/back/test/e2e/src";
      };
      integratesTestrigorE2e = {
        searchPaths.source = [
          outputs."/integrates/web/testrigor/runtime"
        ];
        python = "3.9";
        src = "/integrates/web/testrigor/src";
      };
      integratesBackChartsCollector = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/charts/pypi"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.9";
        src = "/integrates/charts/collector";
      };
      integratesBackCharts = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/charts/pypi"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.9";
        src = "/integrates/charts";
      };
    };
  };
}
