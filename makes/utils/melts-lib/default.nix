{ outputs
, meltsPkgs
, ...
} @ _:
let
  makeTemplate = import (path "/makes/utils/make-template") path meltsPkgs;
in
makeTemplate {
  arguments = {
    envMelts = outputs.apps.melts.program;
    envUtilsBashLibAws = import (path "/makes/utils/bash-lib/aws") path meltsPkgs;
  };
  name = "utils-melts-lib-common";
  template = path "/makes/utils/melts-lib/template.sh";
}
