{ nixpkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  name = "makes-ci-config";
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
