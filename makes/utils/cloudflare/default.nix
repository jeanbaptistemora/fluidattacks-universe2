path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envGrep = "${pkgs.gnugrep}/bin/grep";
    envUtilsAws = import (path "/makes/utils/aws") path pkgs;
    envUtilsSops = import (path "/makes/utils/sops") path pkgs;
  };
  name = "utils-cloudflare";
  template = path "/makes/utils/cloudflare/template.sh";
}
