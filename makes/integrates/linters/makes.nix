{ config
, ...
}:
{
  lintPython = {
    dirsOfModules = {
      integrates = {
        extraSources = [
          config.inputs.product.integrates-back-pypi-runtime
          config.inputs.product.integrates-back-pypi-unit-tests
          config.inputs.product.skims-config-sdk
        ];
        python = "3.7";
        src = "/integrates/back/src";
      };
    };
  };
}
