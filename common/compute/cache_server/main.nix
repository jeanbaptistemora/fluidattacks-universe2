{
  makeScript,
  inputs,
  ...
}: let
  repo = inputs.nixpkgs.fetchFromGitHub {
    owner = "zhaofengli";
    repo = "attic";
    rev = "863f8dcca3efce87a29853f6c842f85de594019e";
    sha256 = "bFzHDHiG5Uwopu/dgje9WNt/KDcxyVinK/k0SYIBtGw=";
  };
  attic_pkg = (inputs.flakeAdapter {src = repo;}).defaultNix;
in
  makeScript {
    name = "cache-server";
    entrypoint = ./entrypoint.sh;
    searchPaths = {
      bin = [
        inputs.nixpkgs.sqlite
        attic_pkg.outputs.packages.${builtins.currentSystem}.attic-server
        attic_pkg.outputs.packages.${builtins.currentSystem}.attic-client
      ];
    };
  }
