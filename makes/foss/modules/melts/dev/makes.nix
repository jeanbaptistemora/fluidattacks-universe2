{ inputs
, makeSearchPaths
, ...
}:
{
  dev = {
    melts = {
      source = [
        inputs.product.melts-config-development
        inputs.product.melts-config-runtime
        (makeSearchPaths {
          pythonPackage = [ "$PWD/melts" ];
        })
      ];
    };
  };
}
