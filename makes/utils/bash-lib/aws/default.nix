pkgs:

let
  makeTemplate = import ../../../../makes/utils/make-template pkgs;
in
  makeTemplate {
    arguments = {
      envAwscli = "${pkgs.awscli}/bin/aws";
    };
    name = "utils-bash-lib-aws";
    template = ../../../../makes/utils/bash-lib/aws/template.sh;
  }
