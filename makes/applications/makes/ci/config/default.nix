{ nixpkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  name = "makes-ci-config";
  arguments = {
    envConfig = path "/makes/applications/makes/ci/src/config.toml";
    envInit = path "/makes/applications/makes/ci/src/init.sh";
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
