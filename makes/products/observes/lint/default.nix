{ observesPkgs
, path
, ...
} @ _:
let
  codePaths = import (path "/makes/lib/observes/package-paths") path;
  localLib = import (path "/makes/lib/observes/local-lib") {
    inherit codePaths;
    pkgs = observesPkgs;
  };
  linter = import (path "/makes/lib/observes/lint-observes");
  lint = packageLib: linter {
    inherit observesPkgs path;
    packageSrcPath = packageLib.packagePath;
    buildInputs = packageLib.buildInputs;
  };
in
builtins.mapAttrs (k: _: lint localLib.${k}) codePaths
