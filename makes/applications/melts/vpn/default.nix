{ makeEntrypoint
, nixpkgs
, path
, ...
}:
makeEntrypoint {
  name = "melts-vpn";
  searchPaths = {
    envPaths = [ nixpkgs.networkmanager ];
  };
  template = path "/makes/applications/melts/vpn/entrypoint.sh";
}
