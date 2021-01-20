path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envJq = "${pkgs.jq}/bin/jq";
    envSops = "${pkgs.sops}/bin/sops";
  };
  name = "utils-bash-lib-sops";
  template = path "/makes/utils/bash-lib/sops/template.sh";
}
