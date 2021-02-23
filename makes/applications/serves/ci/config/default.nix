{ servesPkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path servesPkgs;
in
makeEntrypoint {
  name = "serves-ci-config";
  searchPaths = {
    envPaths = [
      servesPkgs.gnugrep
      servesPkgs.gnused
      servesPkgs.openssh
      servesPkgs.rpl
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/serves/ci/config/entrypoint.sh";
}
