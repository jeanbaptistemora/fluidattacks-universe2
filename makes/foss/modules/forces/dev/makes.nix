{ inputs
, makeSearchPaths
, ...
}:
{
  dev = {
    forces = {
      source = [
        inputs.product.forces-config-development
        inputs.product.forces-config-runtime
        (makeSearchPaths {
          pythonPackage = [ "$PWD/forces" ];
        })
      ];
    };
  };
}
