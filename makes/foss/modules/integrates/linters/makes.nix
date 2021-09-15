{ inputs
, outputs
, ...
}:
{
  lintPython = {
    dirsOfModules = {
      integrates = {
        extraSources = [
          inputs.product.integrates-back-pypi-runtime
          inputs.product.integrates-back-pypi-unit-tests
          inputs.product.skims-config-sdk
        ];
        python = "3.7";
        src = "/integrates/back/src";
      };
      integratesBackChartsGenerators = {
        extraSources = [
          inputs.product.integrates-back-pypi-runtime
          outputs."/integrates/back/charts/pypi"
        ];
        python = "3.7";
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
        extraSources = [
          inputs.product.integrates-back-pypi-runtime
        ];
        python = "3.7";
        src = "/integrates/deploy/permissions_matrix";
      };
      integratesBackMigrations = {
        extraSources = [
          inputs.product.integrates-back-pypi-runtime
        ];
        python = "3.7";
        src = "/integrates/back/migrations";
      };
      integratesBackTests = {
        extraSources = [
          inputs.product.integrates-back-pypi-unit-tests
          inputs.product.integrates-back-pypi-runtime
        ];
        python = "3.7";
        src = "/integrates/back/tests";
      };
      integratesBackTestsE2e = {
        extraSources = [
          inputs.product.integrates-web-e2e-pypi
        ];
        python = "3.7";
        src = "/integrates/back/tests/e2e/src";
      };
    };
  };
}
