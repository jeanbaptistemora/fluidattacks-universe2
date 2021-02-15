{ servesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path servesPkgs;
  name = "serves-ci-config";
  product = "serves";
  target = "serves/ci";
  secretsPath = "serves/secrets/production.yaml";
in
makeEntrypoint {
  arguments = {
    envProduct = product;
    envTarget = target;
    envSecretsPath = secretsPath;
  };
  inherit name;
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
