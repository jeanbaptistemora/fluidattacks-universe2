{ packages
, forcesPkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path forcesPkgs;
in
makeEntrypoint {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path forcesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path forcesPkgs;
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  searchPaths = {
    envPaths = [
      forcesPkgs.jq
      packages.forces
    ];
  };
  name = "forces-process-groups";
  template = path "/makes/applications/forces/process-groups/entrypoint.sh";
}
