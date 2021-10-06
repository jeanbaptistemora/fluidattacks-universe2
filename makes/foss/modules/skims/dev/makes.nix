{ inputs
, makeSearchPaths
, ...
}:
{
  dev = {
    skims = {
      source = [
        inputs.product.skims-config-runtime
        (makeSearchPaths {
          pythonPackage = [ "$PWD/skims/skims" ];
        })
      ];
    };
  };
}
