path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  name = "utils-gitlab";
  searchPaths = {
    envPaths = [
      pkgs.curl
      pkgs.jq
    ];
  };
  template = path "/makes/utils/gitlab/template.sh";
}
