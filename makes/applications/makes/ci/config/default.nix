{ makeEntrypoint
, nixpkgs
, path
, ...
}:
makeEntrypoint {
  name = "makes-ci-config";
  arguments = {
    envConfig = path "/makes/makes/ci/config.toml";
    envInit = path "/makes/makes/ci/init.sh";
  };
  searchPaths = {
    envPaths = [
      nixpkgs.gnugrep
      nixpkgs.gnused
      nixpkgs.openssh
      nixpkgs.rpl
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/makes/ci/config/entrypoint.sh";
}
