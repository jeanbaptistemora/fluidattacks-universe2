{ forcesPkgs
, path
, applications
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path forcesPkgs;
in
makeEntrypoint rec {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path forcesPkgs;
    envForces = applications.forces;
    envJq = forcesPkgs.jq;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path forcesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path forcesPkgs;
  };
  name = "forces-process-groups";
  template = path "/makes/applications/forces/process-groups/entrypoint.sh";
}
