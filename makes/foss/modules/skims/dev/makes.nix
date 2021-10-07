{ makeSearchPaths
, outputs
, ...
}:
{
  dev = {
    skims = {
      source = [
        outputs."/skims/config-runtime"
        (makeSearchPaths {
          pythonPackage = [ "$PWD/skims/skims" ];
        })
      ];
    };
  };
}
