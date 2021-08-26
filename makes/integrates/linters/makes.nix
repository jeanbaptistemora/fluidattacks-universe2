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
    };
    modules = {
      integratesBackCharts = {
        extraSources = [
          inputs.product.integrates-back-pypi-runtime
          outputs."/integrates/back/charts/pypi"
        ];
        python = "3.7";
        src = "/integrates/charts";
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
