attrs @ {
  pkgsSkims,
  ...
}:

let
  makeTemplate = import ../../../../../makes/utils/make-template pkgsSkims;
in
  makeTemplate {
    arguments = {
      envAwscli = "${pkgsSkims.awscli}/bin/aws";
    };
    name = "utils-bash-lib-skims-aws";
    template = ../../../../../makes/utils/bash-lib/skims/aws/template.sh;
  }
