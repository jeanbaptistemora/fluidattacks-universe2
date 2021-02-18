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
, srcReviewsPkgs
, srcServesPkgs
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
      applications = makesPkgs.lib.attrsets.mapAttrsRecursive
        (path: value: "${value}/bin/${builtins.concatStringsSep "-" (makesPkgs.lib.lists.init path)}")
        packages;
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
          attrsByType =
            source: builtins.foldl'
              (x: name: makesPkgs.lib.attrsets.recursiveUpdate x (
                makesPkgs.lib.attrsets.setAttrByPath
                  (makesPkgs.lib.strings.splitString "." name)
                  (import (path "/makes/${source}/${dotToSlash name}") attrs)
              ))
              { }
              (makesPkgs.lib.lists.init (makesPkgs.lib.strings.splitString "\n" (
                builtins.readFile (path "/makes/attrs/${source}.lst"))
              ));
        in
        makesPkgs.lib.attrsets.recursiveUpdate
          (attrsByType "applications")
          (attrsByType "packages");
      packagesFlattened =
        let
          attrsByType = source: builtins.listToAttrs (builtins.map
            (name: {
              inherit name;
              value = import (path "/makes/${source}/${dotToSlash name}") attrs;
            })
            (makesPkgs.lib.lists.init (makesPkgs.lib.strings.splitString "\n" (
              builtins.readFile (path "/makes/attrs/${source}.lst"))
            )));
        in
        attrsByType "applications" // attrsByType "packages";
      path = path: /. + (builtins.unsafeDiscardStringContext self.sourceInfo) + path;
      reviewsPkgs = import srcReviewsPkgs { inherit system; };
      revision = if (builtins.hasAttr "rev" self) then self.rev else "dirty";
      servesPkgs = import srcServesPkgs { inherit system; };
      skimsBenchmarkOwaspRepo = srcSkimsBenchmarkOwaspRepo;
      skimsPkgs = import srcSkimsPkgs { inherit system; };
      skimsPkgsTerraform = import srcSkimsPkgsTerraform { inherit system; };
      skimsTreeSitterRepo = srcSkimsTreeSitterRepo;
      sortsPkgs = import srcSortsPkgs { inherit system; };

      # Makes utils
      buildNodeRequirements = import (path "/makes/utils/build-node-requirements") path;
      buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path;
      getPackageJsonDeps = import (path "/makes/utils/get-package-json-deps") path;
      makeDerivation = import (path "/makes/utils/make-derivation") path;
      makeEntrypoint = import (path "/makes/utils/make-entrypoint") path;
      makeTemplate = import (path "/makes/utils/make-template") path;
    };
    dotToSlash = builtins.replaceStrings [ "." ] [ "/" ];
    makeLazyCopy = attrs: (attrs // {
      copy = makeLazyCopy attrs;
    });
  in
  { packages = attrs.packagesFlattened; }
)
