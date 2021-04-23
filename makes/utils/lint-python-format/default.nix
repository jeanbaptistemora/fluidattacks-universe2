path: pkgs:

{ name
, target
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envSettingsBlack = path "/makes/utils/lint-python-format/settings-black.toml";
    envTarget = target;
  };
  inherit name;
  searchPaths = {
    envPaths = [ pkgs.black ];
  };
  template = path "/makes/utils/lint-python-format/template.sh";
}
