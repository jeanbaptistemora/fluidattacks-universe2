{ meltsPkgs
, outputs
, path
, ...
} @ _:
let
  makeTemplate = import (path "/makes/utils/make-template") path meltsPkgs;
in
makeTemplate {
  arguments = {
    envMelts = outputs.apps.melts.program;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path meltsPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path meltsPkgs;
  };
  name = "utils-melts-lib-common";
  template = path "/makes/libs/melts/template.sh";
}
