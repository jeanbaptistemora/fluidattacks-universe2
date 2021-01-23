path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envGit = "${pkgs.git}/bin/git";
  };
  name = "utils-bash-lib-use-git-workdir";
  template = path "/makes/utils/use-git-workdir/template.sh";
}
