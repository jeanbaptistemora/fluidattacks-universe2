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
    envSettingsIsort = path "/makes/utils/python-format/settings-isort.toml";
    envTargets = nix.asBashArray targets;
  };
  inherit name;
  searchPaths = {
    envPython38Paths = [ pkgs.python38Packages.colorama ];
    envPaths = [
      pkgs.black
      pkgs.git
      pkgs.python38Packages.isort
    ];
  };
  template = path "/makes/utils/python-format/template.sh";
}
