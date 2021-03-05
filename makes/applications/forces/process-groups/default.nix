{ packages
, nixpkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsSops = import (path "/makes/utils/sops") path nixpkgs;
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  searchPaths = {
    envPaths = [
      nixpkgs.jq
      packages.forces
    ];
  };
  name = "forces-process-groups";
  template = path "/makes/applications/forces/process-groups/entrypoint.sh";
}
