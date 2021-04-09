path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  searchPaths = {
    envPaths = [
      pkgs.awscli
    ];
    envUtils = [
      "/makes/utils/env"
    ];
  };
  name = "utils-bash-lib-aws";
  template = path "/makes/utils/aws/template.sh";
}
