path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envGit = "${pkgs.git}/bin/git";
  };
  name = "utils-bash-lib-git";
  template = path "/makes/utils/git/template.sh";
}
