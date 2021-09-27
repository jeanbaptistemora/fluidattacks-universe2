{ inputs
, ...
}:
{
  lintPython = {
    modules = {
      melts = {
        searchPaths.source = [
          inputs.product.melts-config-development
          inputs.product.melts-config-runtime
        ];
        python = "3.8";
        src = "/melts/toolbox";
      };
      meltsTests = {
        searchPaths.source = [
          inputs.product.melts-config-development
          inputs.product.melts-config-runtime
        ];
        python = "3.8";
        src = "/melts/tests";
      };
    };
  };
}
