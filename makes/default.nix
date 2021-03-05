{ self
, srcAirsPkgs
, srcAirsPkgsTerraform
, srcAssertsPkgs
, srcAssertsPkgsTerraform
, srcForcesPkgs
, srcForcesPkgsTerraform
, srcIntegratesMobilePkgs
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
}:
let
  attrs = rec {
    airsPkgs = import srcAirsPkgs { inherit system; };
    airsPkgsTerraform = import srcAirsPkgsTerraform { inherit system; };
    applications = makesPkgs.lib.attrsets.mapAttrsRecursive
      (path: value: "${value}/bin/${builtins.concatStringsSep "-" (makesPkgs.lib.lists.init path)}")
      packages;
    assertsPkgs = import srcAssertsPkgs { inherit system; };
    assertsPkgsTerraform = import srcAssertsPkgsTerraform { inherit system; };
    debug = value: builtins.trace value value;
    forcesPkgs = import srcForcesPkgs { inherit system; };
    forcesPkgsTerraform = import srcForcesPkgsTerraform { inherit system; };
    integratesMobilePkgs = import srcIntegratesMobilePkgs { inherit system; config.android_sdk.accept_license = true; };
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
    system = "x86_64-linux";
    skimsBenchmarkOwaspRepo = srcSkimsBenchmarkOwaspRepo;
    skimsPkgs = import srcSkimsPkgs { inherit system; };
    skimsPkgsTerraform = import srcSkimsPkgsTerraform { inherit system; };
    skimsTreeSitterRepo = srcSkimsTreeSitterRepo;
    sortsPkgs = import srcSortsPkgs { inherit system; };

    # Makes utilities
    buildNodeRequirements = import (path "/makes/utils/build-node-requirements") path;
    buildPythonLambda = import (path "/makes/utils/build-python-lambda") path;
    buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path;
    computeOnAws = import (path "/makes/utils/compute-on-aws") path;
    getPackageJsonDeps = import (path "/makes/utils/get-package-json-deps") path;
    lintPython = import (path "/makes/utils/lint-python") path;
    makeDerivation = import (path "/makes/utils/make-derivation") path;
    makeEntrypoint = import (path "/makes/utils/make-entrypoint") path;
    makeOci = import (path "/makes/utils/make-oci") path;
    makeSearchPaths = import (path "/makes/utils/make-search-paths") path;
    makeTemplate = import (path "/makes/utils/make-template") path;
    nix = import (path "/makes/utils/nix") path makesPkgs;
    ociDeploy = import (path "/makes/utils/oci-deploy") path;
    terraformApply = import (path "/makes/utils/terraform-apply") path;
    terraformTest = import (path "/makes/utils/terraform-test") path;
  };
  dotToSlash = builtins.replaceStrings [ "." ] [ "/" ];
in
{ packages.x86_64-linux = attrs.packagesFlattened; }
