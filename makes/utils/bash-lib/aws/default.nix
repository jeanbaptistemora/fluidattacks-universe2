path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envAwscli = "${pkgs.awscli}/bin/aws";
  };
  name = "utils-bash-lib-aws";
  template = path "/makes/utils/bash-lib/aws/template.sh";
}
