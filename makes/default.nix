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
      url = "https://github.com/owasp/benchmark/archive/1cfe52ea6dc49bebae12e6ceb20356196f0e9ac8.tar.gz";
      sha256 = "pcNMJJJ2cRxh4Kgq0ElOIyBJemJu4qggxY3Debjbcms=";
    };
    skimsNISTTestSuites = fetchzip {
      url = "https://github.com/fluidattacks/NIST-SARD-Test-Suites/archive/7189c65ab6e398180e3f2aa2de683466b4412821.tar.gz";
      sha256 = "CDLX3Xa7nCmzdJdAjlSzdlFIaUx3cg7GPiqc5c8Dj6Q=";
    };
    skimsVulnerableAppRepo = fetchzip {
      url = "https://github.com/SasanLabs/VulnerableApp/archive/f5334e84faadbfb4beec42849a2e8acc5e37a276.tar.gz";
      sha256 = "gVY9VPo0+2xHdbME61MH/JaMP8pyqWh5k7im3O8hNAc=";
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
    bashFormat = importUtility "bash-format";
    buildNodeRequirements = importUtility "build-node-requirements";
    buildPythonLambda = importUtility "build-python-lambda";
    buildPythonPackage = importUtility "build-python-package";
    buildPythonRequirements = importUtility "build-python-requirements";
    buildRubyRequirement = importUtility "build-ruby-requirement";
    bundleClosure = importUtility "bundle-closure";
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
    pythonFormat = importUtility "python-format";
    terraformApply = importUtility "terraform-apply";
    terraformTest = importUtility "terraform-test";
  };
in
{ packages.x86_64-linux = attrs.packagesFlattened; }
