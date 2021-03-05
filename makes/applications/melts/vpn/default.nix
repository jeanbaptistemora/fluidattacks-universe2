{ nixpkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envNetworkManager = nixpkgs.networkmanager;
  };
  name = "melts-vpn";
  template = path "/makes/applications/melts/vpn/entrypoint.sh";
}
