{ makeSearchPaths
, outputs
, inputs
, ...
}:
{
  dev = {
    melts = {
      source = [
        outputs."/melts/config-development"
        inputs.product.melts-config-runtime
        (makeSearchPaths {
          pythonPackage = [ "$PWD/melts" ];
        })
      ];
    };
  };
}
