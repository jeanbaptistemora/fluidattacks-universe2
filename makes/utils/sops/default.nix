path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  searchPaths = {
    envPaths = [
      pkgs.jq
      pkgs.sops
    ];
  };
  name = "utils-bash-lib-sops";
  template = path "/makes/utils/sops/template.sh";
}
