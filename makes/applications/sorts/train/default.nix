{ packages
, path
, nixpkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envPython = "${nixpkgs.python38}/bin/python";
    envSetupSortsDevelopment = packages.sorts.config-development;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs;
  };
  name = "sorts-train";
  template = path "/makes/applications/sorts/train/entrypoint.sh";
}
