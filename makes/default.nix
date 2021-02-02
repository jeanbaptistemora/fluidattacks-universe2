{ flakeUtils
, self
, srcForcesPkgs
, srcIntegratesPkgs
, srcIntegratesPkgsTerraform
, srcMakesPkgs
, srcMeltsPkgs
, srcObservesPkgs
, srcObservesPkgsTerraform
, srcSkimsBenchmarkOwaspRepo
, srcSkimsPkgs
, srcSkimsPkgsTerraform
, srcSkimsTreeSitterRepo
, srcSortsPkgs
, ...
} @ _:

flakeUtils.lib.eachSystem [ "x86_64-linux" ] (
  system:
  let
    attrs = makeLazyCopy rec {
      debug = value: builtins.trace value value;
      forcesPkgs = import srcForcesPkgs { inherit system; };
      integratesPkgs = import srcIntegratesPkgs { inherit system; };
      integratesPkgsTerraform = import srcIntegratesPkgsTerraform { inherit system; };
      makesPkgs = import srcMakesPkgs { inherit system; };
      meltsPkgs = import srcMeltsPkgs { inherit system; };
      observesPkgs = import srcObservesPkgs { inherit system; };
      observesPkgsTerraform = import srcObservesPkgsTerraform { inherit system; };
      outputs = {
        apps = builtins.mapAttrs makeApp sources.apps;
        packages = sources.packages;
      };
      path = path: /. + (builtins.unsafeDiscardStringContext self.sourceInfo) + path;
      skimsBenchmarkOwaspRepo = srcSkimsBenchmarkOwaspRepo;
      skimsPkgs = import srcSkimsPkgs { inherit system; };
      skimsPkgsTerraform = import srcSkimsPkgsTerraform { inherit system; };
      skimsTreeSitterRepo = srcSkimsTreeSitterRepo;
      sortsPkgs = import srcSortsPkgs { inherit system; };
      sources =
        let
          attrsByType = source: builtins.listToAttrs (builtins.map
            (name: {
              inherit name;
              value = import (path "/makes/${source}/${name}") attrs;
            })
            (makesPkgs.lib.lists.init (makesPkgs.lib.strings.splitString "\n" (
              builtins.readFile (path "/makes/attrs/${source}.lst"))
            )));
        in
        {
          apps = attrsByType "applications";
          packages = attrsByType "packages";
        };
    };
    makeApp = app: derivation: {
      program = "${derivation}/bin/${builtins.replaceStrings [ "/" ] [ "-" ] app}";
      type = "app";
    };
    makeLazyCopy = attrs: (attrs // {
      copy = makeLazyCopy attrs;
    });
  in
  attrs.outputs
)
