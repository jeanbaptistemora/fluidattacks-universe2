{ applications
, path
, nixpkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envSkimsProcessGroupOnAws = applications.skims.process-group-on-aws;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsBashLibGit = import (path "/makes/utils/git") path nixpkgs;
  };
  name = "skims-process-groups-on-aws";
  template = path "/makes/applications/skims/process-groups-on-aws/entrypoint.sh";
}
