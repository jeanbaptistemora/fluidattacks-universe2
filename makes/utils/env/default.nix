path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  name = "utils-env";
  searchPaths = {
    envPaths = [
      pkgs.curl
      pkgs.jq
    ];
    envUtils = [
      "/makes/utils/gitlab"
    ];
  };
  template = path "/makes/utils/env/template.sh";
}
