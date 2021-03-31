{ self
, nixpkgsSource
, nixpkgsSource2
, nixpkgsSource3
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
      url = "https://github.com/owasp/benchmark/archive/b38d197949f775b3c165029bda9dc6bd890265fb.tar.gz";
      sha256 = "vAWzTEc48sny46Y+hsv7yw1gNoQ9rBO6JL07RejRoUw=";
    };

    # Nix packages
    nixpkgs = import nixpkgsSource {
      config.allowUnfree = true;
      config.android_sdk.accept_license = true;
      inherit system;
    };
    nixpkgs2 = import nixpkgsSource2 { inherit system; };
    nixpkgs3 = import nixpkgsSource3 {
      config.allowUnfree = true;
      inherit system;
    };

    # Makes utilities
    buildNodeRequirements = importUtility "build-node-requirements";
    buildPythonLambda = importUtility "build-python-lambda";
    buildPythonPackage = importUtility "build-python-package";
    buildPythonRequirements = importUtility "build-python-requirements";
    buildRubyRequirement = importUtility "build-ruby-requirement";
    computeOnAws = importUtility "compute-on-aws";
    fetchurl = nixpkgs.fetchurl;
    fetchzip = nixpkgs.fetchzip;
    getPackageJsonDeps = importUtility "get-package-json-deps";
    lintPython = importUtility "lint-python";
    lintTypescript = importUtility "lint-typescript";
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
