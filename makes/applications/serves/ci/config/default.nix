{ nixpkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  name = "serves-ci-config";
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
  template = path "/makes/applications/serves/ci/config/entrypoint.sh";
}
