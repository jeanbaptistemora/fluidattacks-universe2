{ nixpkgs
, path
, ...
}:
let
  nixPkgs = nixpkgs;

  localLib = import (path "/makes/libs/observes/packages") {
    inherit nixPkgs path;
  };

  pythonLinter = import (path "/makes/libs/observes/linter");
  lint = observesPackage: pythonLinter {
    inherit nixPkgs observesPackage path;
  };
  jobs.lint = builtins.mapAttrs (k: _: lint localLib.${k}) localLib;

  pythonTester = import (path "/makes/libs/observes/tester");
  test = observesPackage: pythonTester {
    inherit nixPkgs observesPackage path;
    testDir = "tests";
  };
  jobs.test = builtins.mapAttrs (k: _: test localLib.${k}) localLib;

  binaries = import (path "/makes/libs/observes/bins") {
    inherit nixPkgs path;
  };
in
{
  inherit binaries;
  inherit jobs;
  packages = localLib;
}
