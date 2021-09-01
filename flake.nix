{
  description = "Fluid Attacks, We hack your software!";
  inputs = {
    flakeCompat = { url = "github:edolstra/flake-compat"; flake = false; };
    makesSource = { url = "github:fluidattacks/makes"; flake = false; };
    nixpkgsSource = { url = "https://github.com/nixos/nixpkgs/archive/932941b79c3dbbef2de9440e1631dfec43956261.tar.gz"; flake = false; };
    nixpkgsSource2 = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    nixpkgsSource3 = { url = "https://github.com/nixos/nixpkgs/archive/a1d64d9419422ae9779ab5cada5828127a24e100.tar.gz"; flake = false; };
  };
  outputs =
    { self
    , makesSource
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

        makes = import "${makesSource}/src/args/agnostic.nix" {
          inherit system;
        };

        # Nix packages
        nixpkgs = import nixpkgsSource {
          config.allowUnfree = true;
          config.android_sdk.accept_license = true;
          overlays = nixpkgsOverlays;
          inherit system;
        };
        nixpkgs2 = import nixpkgsSource2 { inherit system; };
        nixpkgs3 = import nixpkgsSource3 {
          config.allowUnfree = true;
          inherit system;
        };
        nixpkgsOverlays = [
          (_: supper: {
            # Nginx by default tries to use directories owned by root
            # We have to recompile it pointing to the user-space
            nginxLocal = supper.nginx.overrideAttrs (attrs: {
              configureFlags = attrs.configureFlags ++ [
                "--error-log-path=/tmp/error.log"
                "--http-client-body-temp-path=/tmp/nginx_client_body"
                "--http-fastcgi-temp-path=/tmp/nginx_fastcgi"
                "--http-log-path=/tmp/access.log"
                "--http-proxy-temp-path=/tmp/nginx_proxy"
                "--http-scgi-temp-path=/tmp/nginx_scgi"
                "--http-uwsgi-temp-path=/tmp/nginx_uwsgi"
              ];
            });
          })
        ];

        # Makes utilities
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
        lintTypescript = importUtility "lint-typescript";
        makeDerivation = importUtility "make-derivation";
        makeEntrypoint = importUtility "make-entrypoint";
        makeOci = importUtility "make-oci";
        makeSearchPaths = importUtility "make-search-paths";
        makeTemplate = importUtility "make-template";
        nix = importUtility "nix";
        sslCerts = importUtility "ssl-certs";
        terraformApply = importUtility "terraform-apply";
        terraformTest = importUtility "terraform-test";
      };
    in
    { packages.x86_64-linux = attrs.packagesFlattened; };
}
