{ meltsPkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envNetworkManager = meltsPkgs.networkmanager;
  };
  name = "melts-vpn";
  template = path "/makes/applications/melts/vpn/entrypoint.sh";
}
