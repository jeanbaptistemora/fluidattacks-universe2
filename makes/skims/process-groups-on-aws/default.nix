{ outputs
, path
, skimsPkgs
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envSkimsProcessGroupOnAws = outputs.apps.skims-process-group-on-aws.program;
    envUtilsBashLibAws = import (path "/makes/utils/bash-lib/aws") skimsPkgs;
    envUtilsBashLibUseGitRepo = import (path "/makes/utils/bash-lib/use-git-repo") skimsPkgs;
  };
  location = "/bin/skims-process-groups-on-aws";
  name = "skims-process-groups-on-aws";
  template = (path "/makes/skims/process-groups-on-aws/entrypoint.sh");
}
