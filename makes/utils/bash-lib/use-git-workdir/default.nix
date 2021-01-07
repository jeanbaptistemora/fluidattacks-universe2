pkgs:
let
  makeTemplate = import ../../../../makes/utils/make-template pkgs;
in
makeTemplate {
  arguments = {
    envGit = "${pkgs.git}/bin/git";
  };
  name = "utils-bash-lib-use-git-workdir";
  template = ../../../../makes/utils/bash-lib/use-git-workdir/template.sh;
}
