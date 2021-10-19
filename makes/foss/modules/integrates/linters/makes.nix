{ outputs
, ...
}:
{
  lintPython = {
    dirsOfModules = {
      integrates = {
        searchPaths.source = [
          outputs."/integrates/back/pypi/runtime"
          outputs."/integrates/back/pypi/unit-tests"
        ];
        python = "3.9";
        src = "/integrates/back/src";
      };
      integratesBackChartsGenerators = {
        searchPaths.source = [
          outputs."/integrates/back/pypi/runtime"
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
          outputs."/integrates/back/pypi/runtime"
        ];
        python = "3.9";
        src = "/integrates/deploy/permissions_matrix";
      };
      integratesBackMigrations = {
        searchPaths.source = [
          outputs."/integrates/back/pypi/runtime"
        ];
        python = "3.9";
        src = "/integrates/back/migrations";
      };
      integratesBackTests = {
        searchPaths.source = [
          outputs."/integrates/back/pypi/unit-tests"
          outputs."/integrates/back/pypi/runtime"
        ];
        python = "3.9";
        src = "/integrates/back/tests";
      };
      integratesBackTestsE2e = {
        searchPaths.source = [
          outputs."/integrates/web/e2e/pypi"
        ];
        python = "3.9";
        src = "/integrates/back/tests/e2e/src";
      };
    };
  };
}
