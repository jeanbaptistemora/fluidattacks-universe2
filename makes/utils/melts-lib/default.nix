{ outputs
, meltsPkgs
, ...
} @ _:
let
  makeTemplate = import ../../../makes/utils/make-template meltsPkgs;
in
makeTemplate {
  arguments = {
    envMelts = outputs.apps.melts.program;
    envUtilsBashLibAws = import ../../../makes/utils/bash-lib/aws meltsPkgs;
  };
  name = "utils-melts-lib-common";
  template = ../../../makes/utils/melts-lib/template.sh;
}
