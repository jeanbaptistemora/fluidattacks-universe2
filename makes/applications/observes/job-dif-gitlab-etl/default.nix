{ applications
, observesPkgs
, path
, ...
}:
let
  nixPkgs = observesPkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = {
    envDifGitlabEtl = applications.observes.dif-gitlab-etl;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixPkgs;
  };
  name = "observes-job-dif-gitlab-etl";
  template = path "/makes/applications/observes/job-dif-gitlab-etl/entrypoint.sh";
}
