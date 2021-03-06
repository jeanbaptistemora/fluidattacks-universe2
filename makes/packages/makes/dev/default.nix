{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
makeTemplate {
  arguments = {
    envSkimsSetupDevelopment = packages.skims.config-development;
    envSkimsSetupRuntime = packages.skims.config-runtime;
  };
  name = "makes-dev";
  searchPaths = {
    envPaths = [
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
  };
  template = path "/makes/packages/makes/dev/template.sh";
}
