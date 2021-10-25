{ outputs
, inputs
, ...
}:
{
  lintPython = {
    modules = {
      melts = {
        searchPaths.source = [
          outputs."/melts/config-development"
          inputs.product.melts-config-runtime
        ];
        python = "3.8";
        src = "/melts/toolbox";
      };
      meltsTests = {
        searchPaths.source = [
          outputs."/melts/config-development"
          inputs.product.melts-config-runtime
        ];
        python = "3.8";
        src = "/melts/tests";
      };
    };
  };
}
