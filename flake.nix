{
  description = "Fluid Attacks, We hack your software!";
  inputs = {
    flakeCompat = { url = "github:edolstra/flake-compat"; flake = false; };
    makes = { url = "github:fluidattacks/makes"; };
    nixpkgsSource = { url = "https://github.com/nixos/nixpkgs/archive/932941b79c3dbbef2de9440e1631dfec43956261.tar.gz"; flake = false; };
    nixpkgsSource2 = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    nixpkgsSource3 = { url = "https://github.com/nixos/nixpkgs/archive/a1d64d9419422ae9779ab5cada5828127a24e100.tar.gz"; flake = false; };
  };
  outputs =
    { self
    , makes
    , nixpkgsSource
    , nixpkgsSource2
    , nixpkgsSource3
    , ...
    } @ inputs:
    let
      system = "x86_64-linux";

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
        inherit system;

        makes = import "${inputs.makes.sourceInfo}/src/args/agnostic.nix" {
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
        computeOnAws = importUtility "compute-on-aws";
        fetchurl = nixpkgs.fetchurl;
        fetchzip = nixpkgs.fetchzip;
        lintTypescript = importUtility "lint-typescript";
        makeDerivation = importUtility "make-derivation";
        makeEntrypoint = importUtility "make-entrypoint";
        makeSearchPaths = importUtility "make-search-paths";
        makeTemplate = importUtility "make-template";
        nix = importUtility "nix";
        sslCerts = importUtility "ssl-certs";
      };
    in
    (
      (makes.lib.flakes.evaluate {
        inputs = {
          inherit self;
        };
        inherit system;
      }) //
      { packages.x86_64-linux = attrs.packagesFlattened; }
    );
}
