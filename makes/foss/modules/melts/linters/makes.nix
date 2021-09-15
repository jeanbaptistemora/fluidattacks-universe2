{ inputs
, ...
}:
{
  lintPython = {
    modules = {
      melts = {
        extraSources = [
          inputs.product.melts-config-development
          inputs.product.melts-config-runtime
        ];
        python = "3.8";
        src = "/melts/toolbox";
      };
      meltsTests = {
        extraSources = [
          inputs.product.melts-config-development
          inputs.product.melts-config-runtime
        ];
        python = "3.8";
        src = "/melts/tests";
      };
    };
  };
}
