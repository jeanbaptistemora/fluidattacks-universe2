path: pkgs:

{ name
, targets
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
  nix = import (path "/makes/utils/nix") path pkgs;
in
makeEntrypoint {
  arguments = {
    envTargets = nix.asBashArray targets;
  };
  inherit name;
  searchPaths = {
    envPaths = [
      pkgs.shfmt
    ];
  };
  template = path "/makes/utils/bash-format/template.sh";
}
