pkgs:

let
  makeTemplate = import ../../../../makes/utils/make-template pkgs;
in
  makeTemplate {
    arguments = {
      envJq = "${pkgs.jq}/bin/jq";
      envSops = "${pkgs.sops}/bin/sops";
    };
    name = "utils-bash-lib-sops";
    template = ../../../../makes/utils/bash-lib/sops/template.sh;
  }
