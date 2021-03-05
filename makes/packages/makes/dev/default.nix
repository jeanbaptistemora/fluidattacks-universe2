{ nixpkgs
, packages
, path
, ...
}:
let
  makeTemplate = import (path "/makes/utils/make-template") path nixpkgs;
in
makeTemplate {
  arguments = {
    envBaseSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path nixpkgs [
      nixpkgs.awscli
      nixpkgs.cloc
      nixpkgs.jq
      nixpkgs.nixpkgs-fmt
      nixpkgs.redis
      nixpkgs.sops
      nixpkgs.terraform
      nixpkgs.tokei
      nixpkgs.yq
    ];
    envSkimsSetupDevelopment = packages.skims.config-development;
    envSkimsSetupRuntime = packages.skims.config-runtime;
  };
  name = "makes-dev";
  template = path "/makes/packages/makes/dev/template.sh";
}
