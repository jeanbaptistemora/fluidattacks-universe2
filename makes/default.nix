{ self
, nixpkgsSource
, nixpkgsSource2
, ...
}:
let
  attrs = rec {
    applications = nixpkgs.lib.attrsets.mapAttrsRecursive
      (path: value: "${value}/bin/${builtins.concatStringsSep "-" (nixpkgs.lib.lists.init path)}")
      packages;
    debug = value: builtins.trace value value;
    dotToSlash = builtins.replaceStrings [ "." ] [ "/" ];
    importUtility = utility: import (path "/makes/utils/${utility}") path nixpkgs;
    packages =
      let
        attrsByType =
          source: builtins.foldl'
            (x: name: nixpkgs.lib.attrsets.recursiveUpdate x (
              nixpkgs.lib.attrsets.setAttrByPath
                (nixpkgs.lib.strings.splitString "." name)
                (import (path "/makes/${source}/${dotToSlash name}") attrs)
            ))
            { }
            (nixpkgs.lib.lists.init (nixpkgs.lib.strings.splitString "\n" (
              builtins.readFile (path "/makes/attrs/${source}.lst"))
            ));
      in
      nixpkgs.lib.attrsets.recursiveUpdate
        (attrsByType "applications")
        (attrsByType "packages");
    packagesFlattened =
      let
        attrsByType = source: builtins.listToAttrs (builtins.map
          (name: {
            inherit name;
            value = import (path "/makes/${source}/${dotToSlash name}") attrs;
          })
          (nixpkgs.lib.lists.init (nixpkgs.lib.strings.splitString "\n" (
            builtins.readFile (path "/makes/attrs/${source}.lst"))
          )));
      in
      attrsByType "applications" // attrsByType "packages";
    path = path: /. + (builtins.unsafeDiscardStringContext self.sourceInfo) + path;
    revision = if (builtins.hasAttr "rev" self) then self.rev else "dirty";
    system = "x86_64-linux";
    skimsBenchmarkOwaspRepo = fetchzip {
      url = "https://github.com/owasp/benchmark/archive/9a0c25a5f8443245c676965d20d22d5f93da3f99.tar.gz";
      sha256 = "QwtG90KPleNRU9DrNYTdBlcjR6vcmLTiC6G57x1Ayw4=";
    };

    # Nix packages
    nixpkgs = import nixpkgsSource { inherit system; };
    nixpkgs2 = import nixpkgsSource2 { inherit system; config.android_sdk.accept_license = true; };

    # Makes utilities
    buildNodeRequirements = importUtility "build-node-requirements";
    buildPythonLambda = importUtility "build-python-lambda";
    buildPythonRequirements = importUtility "build-python-requirements";
    computeOnAws = importUtility "compute-on-aws";
    fetchzip = nixpkgs.fetchzip;
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
