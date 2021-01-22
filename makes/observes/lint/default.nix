{ observesPkgs
, path
, ...
} @ _:
let
  codePaths = import (path "/makes/utils/observes-lib/package-paths") path;
  localLib = import (path "/makes/utils/observes-lib/local-lib") {
    inherit codePaths;
    pkgs = observesPkgs;
  };
  linter = import (path "/makes/utils/observes-lib/lint-observes");
  lint = packageLib: linter {
    inherit observesPkgs path;
    packageSrcPath = packageLib.packagePath;
    buildInputs = packageLib.buildInputs;
  };
in
builtins.mapAttrs (k: _: lint localLib.${k}) codePaths
