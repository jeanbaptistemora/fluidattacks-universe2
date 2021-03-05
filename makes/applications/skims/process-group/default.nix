{ applications
, packages
, path
, nixpkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envJq = "${nixpkgs.jq}/bin/jq";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsBashLibGit = import (path "/makes/utils/git") path nixpkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixpkgs;
    envSetupSkimsRuntime = packages.skims.config-runtime;
    envMelts = applications.melts;
    envSkims = applications.skims;
    envTee = "${nixpkgs.coreutils}/bin/tee";
    envYq = "${nixpkgs.yq}/bin/yq";
  };
  name = "skims-process-group";
  template = path "/makes/applications/skims/process-group/entrypoint.sh";
}
