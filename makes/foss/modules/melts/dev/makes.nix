{ makeSearchPaths
, outputs
, ...
}:
{
  dev = {
    melts = {
      source = [
        outputs."/melts/config-development"
        outputs."/melts/config-runtime"
        (makeSearchPaths {
          pythonPackage = [ "$PWD/melts" ];
        })
      ];
    };
  };
}
