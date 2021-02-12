path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  name = "utils-cloudflare";
  searchPaths = {
    envPaths = [
      pkgs.gnugrep
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/utils/cloudflare/template.sh";
}
