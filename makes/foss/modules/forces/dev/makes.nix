{ makeSearchPaths
, outputs
, ...
}:
{
  dev = {
    forces = {
      source = [
        outputs."/forces/config-development"
        outputs."/forces/config-runtime"
        (makeSearchPaths {
          pythonPackage = [ "$PWD/forces" ];
        })
      ];
    };
  };
}
