path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envConfig = path "/makes/utils/lint-typescript/";
  };
  name = "utils-bash-lib-lint-typescript";
  template = path "/makes/utils/lint-typescript/template.sh";
}
