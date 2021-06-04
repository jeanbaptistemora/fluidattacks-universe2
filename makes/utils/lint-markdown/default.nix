path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envStyle = path "/makes/utils/lint-markdown/style.rb";
  };
  searchPaths = {
    envPaths = [
      pkgs.mdl
    ];
  };
  name = "utils-bash-lib-lint-markdown";
  template = path "/makes/utils/lint-markdown/template.sh";
}
