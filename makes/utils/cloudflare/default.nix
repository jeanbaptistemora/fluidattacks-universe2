path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  searchPaths = {
    envPaths = [
      pkgs.curl
      pkgs.jq
    ];
    envUtils = [ ];
  };
  name = "utils-cloudflare";
  template = path "/makes/utils/cloudflare/template.sh";
}
