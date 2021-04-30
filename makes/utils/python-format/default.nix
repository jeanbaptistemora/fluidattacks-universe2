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
    envSettingsBlack = path "/makes/utils/python-format/settings-black.toml";
    envTargets = nix.asBashArray targets;
  };
  inherit name;
  searchPaths = {
    envPaths = [ pkgs.black ];
  };
  template = path "/makes/utils/python-format/template.sh";
}
