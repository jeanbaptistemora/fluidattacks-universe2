path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  name = "makes-utils-time";
  template = path "/makes/utils/time/template.sh";
}
