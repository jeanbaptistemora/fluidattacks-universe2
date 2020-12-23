pkgs:

let
  makeTemplate = import ../../../../../makes/utils/make-template pkgs;
in
  makeTemplate {
    arguments = {
      envAwscli = "${pkgs.awscli}/bin/aws";
    };
    name = "utils-bash-lib-skims-aws";
    template = ../../../../../makes/utils/bash-lib/skims/aws/template.sh;
  }
