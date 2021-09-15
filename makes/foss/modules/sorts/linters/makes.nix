{ inputs
, ...
}:
{
  lintPython = {
    dirsOfModules = {
      sorts = {
        extraSources = [
          inputs.product.sorts-config-development
          inputs.product.sorts-config-runtime
        ];
        python = "3.8";
        src = "/sorts/sorts";
      };
    };
    imports = {
      sorts = {
        config = "/sorts/setup.imports.cfg";
        src = "/sorts/sorts";
      };
    };
    modules = {
      sortsTests = {
        extraSources = [
          inputs.product.sorts-config-development
          inputs.product.sorts-config-runtime
        ];
        python = "3.8";
        src = "/sorts/test";
      };
      sortsTraining = {
        extraSources = [
          inputs.product.sorts-config-development
          inputs.product.sorts-config-runtime
        ];
        python = "3.8";
        src = "/sorts/training";
      };
    };
  };
}
