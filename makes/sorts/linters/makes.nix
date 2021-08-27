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
  };
}
