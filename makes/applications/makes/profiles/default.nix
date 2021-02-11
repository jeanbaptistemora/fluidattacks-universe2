{ makesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path makesPkgs;
  makeProfileScript = envPackages: makeTemplate {
    arguments = { inherit envPackages; };
    name = "makes-profile-template";
    template = path "/makes/applications/makes/profiles/template.sh";
  };
in
makeEntrypoint {
  arguments = {
    envHacker = makeProfileScript [
      "melts-vpn"
      "melts"
      "sorts"
      "skims"
    ];
  };
  name = "makes-profiles";
  template = path "/makes/applications/makes/profiles/entrypoint.sh";
}
