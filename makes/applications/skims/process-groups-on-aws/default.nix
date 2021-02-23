{ applications
, path
, skimsPkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envSkimsProcessGroupOnAws = applications.skims.process-group-on-aws;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path skimsPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/git") path skimsPkgs;
  };
  name = "skims-process-groups-on-aws";
  template = path "/makes/applications/skims/process-groups-on-aws/entrypoint.sh";
}
