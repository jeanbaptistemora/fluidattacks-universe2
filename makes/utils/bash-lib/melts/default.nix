{ outputs
, meltsPkgs
, ...
} @ _:
let
  makeTemplate = import ../../../../makes/utils/make-template meltsPkgs;
in
makeTemplate {
  arguments = {
    envMelts = outputs.apps.melts.program;
  };
  name = "utils-bash-lib-melts";
  template = ../../../../makes/utils/bash-lib/melts/template.sh;
}
