{ flakeUtils
, self
, srcForcesPkgs
, srcForcesPkgsTerraform
, srcIntegratesPkgs
, srcIntegratesPkgsTerraform
, srcMakesPkgs
, srcMeltsPkgs
, srcObservesPkgs
, srcObservesPkgsTerraform
, srcServesPkgsTerraform
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
      applications = builtins.mapAttrs (name: value: "${value}/bin/${slashToDash name}") packages;
      debug = value: builtins.trace value value;
      forcesPkgs = import srcForcesPkgs { inherit system; };
      forcesPkgsTerraform = import srcForcesPkgsTerraform { inherit system; };
      integratesPkgs = import srcIntegratesPkgs { inherit system; };
      integratesPkgsTerraform = import srcIntegratesPkgsTerraform { inherit system; };
      makesPkgs = import srcMakesPkgs { inherit system; };
      meltsPkgs = import srcMeltsPkgs { inherit system; };
      observesPkgs = import srcObservesPkgs { inherit system; };
      observesPkgsTerraform = import srcObservesPkgsTerraform { inherit system; };
      packages =
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
        attrsByType "applications" // attrsByType "packages";
      path = path: /. + (builtins.unsafeDiscardStringContext self.sourceInfo) + path;
      revision = if (builtins.hasAttr "rev" self) then self.rev else "dirty";
      servesPkgsTerraform = import srcServesPkgsTerraform { inherit system; };
      skimsBenchmarkOwaspRepo = srcSkimsBenchmarkOwaspRepo;
      skimsPkgs = import srcSkimsPkgs { inherit system; };
      skimsPkgsTerraform = import srcSkimsPkgsTerraform { inherit system; };
      skimsTreeSitterRepo = srcSkimsTreeSitterRepo;
      sortsPkgs = import srcSortsPkgs { inherit system; };
    };
    slashToDash = builtins.replaceStrings [ "/" ] [ "-" ];
    makeLazyCopy = attrs: (attrs // {
      copy = makeLazyCopy attrs;
    });
  in
  { inherit (attrs) packages; }
)
