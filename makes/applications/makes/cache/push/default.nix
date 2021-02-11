{ makesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
in
makeEntrypoint {
  arguments = {
    envNix = "${makesPkgs.nix}/bin/nix";
    envSsh = makesPkgs.openssh;
  };
  name = "makes-cache-push";
  template = path "/makes/applications/makes/cache/push/entrypoint.sh";
}
