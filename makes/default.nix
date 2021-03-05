{ self
, srcAirsPkgs
, srcAssertsPkgs
, srcForcesPkgs
, srcIntegratesMobilePkgs
, srcIntegratesPkgs
, srcMakesPkgs
, srcMeltsPkgs
, srcObservesPkgs
, srcReviewsPkgs
, srcServesPkgs
, srcSkimsPkgs
, srcSortsPkgs
, ...
}:
let
  attrs = rec {
    airsPkgs = import srcAirsPkgs { inherit system; };
    applications = makesPkgs.lib.attrsets.mapAttrsRecursive
      (path: value: "${value}/bin/${builtins.concatStringsSep "-" (makesPkgs.lib.lists.init path)}")
      packages;
    assertsPkgs = import srcAssertsPkgs { inherit system; };
    debug = value: builtins.trace value value;
    dotToSlash = builtins.replaceStrings [ "." ] [ "/" ];
    forcesPkgs = import srcForcesPkgs { inherit system; };
    importUtility = utility: import (path "/makes/utils/${utility}") path makesPkgs;
    integratesMobilePkgs = import srcIntegratesMobilePkgs { inherit system; config.android_sdk.accept_license = true; };
    integratesPkgs = import srcIntegratesPkgs { inherit system; };
    makesPkgs = import srcMakesPkgs { inherit system; };
    meltsPkgs = import srcMeltsPkgs { inherit system; };
    observesPkgs = import srcObservesPkgs { inherit system; };
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
    skimsBenchmarkOwaspRepo = fetchzip {
      url = "https://github.com/owasp/benchmark/archive/9a0c25a5f8443245c676965d20d22d5f93da3f99.tar.gz";
      sha256 = "QwtG90KPleNRU9DrNYTdBlcjR6vcmLTiC6G57x1Ayw4=";
    };
    skimsPkgs = import srcSkimsPkgs { inherit system; };
    sortsPkgs = import srcSortsPkgs { inherit system; };

    # Makes utilities
    buildNodeRequirements = importUtility "build-node-requirements";
    buildPythonLambda = importUtility "build-python-lambda";
    buildPythonRequirements = importUtility "build-python-requirements";
    computeOnAws = importUtility "compute-on-aws";
    fetchzip = makesPkgs.fetchzip;
    getPackageJsonDeps = importUtility "get-package-json-deps";
    lintPython = importUtility "lint-python";
    makeDerivation = importUtility "make-derivation";
    makeEntrypoint = importUtility "make-entrypoint";
    makeOci = importUtility "make-oci";
    makeSearchPaths = importUtility "make-search-paths";
    makeTemplate = importUtility "make-template";
    nix = importUtility "nix";
    ociDeploy = importUtility "oci-deploy";
    terraformApply = importUtility "terraform-apply";
    terraformTest = importUtility "terraform-test";
  };
in
{ packages.x86_64-linux = attrs.packagesFlattened; }
