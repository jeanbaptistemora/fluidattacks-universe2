{fetchNixpkgs}: let
  system = "x86_64-linux";
  python_version = "python38";
  nixpkgs = fetchNixpkgs {
    rev = "97bdf4893d643e47d2bd62e9a2ec77c16ead6b9f";
    sha256 = "pOglCsO0/pvfHvVEb7PrKhnztYYNurZZKrc9YfumhJQ=";
  };
  out = import ./. {
    inherit nixpkgs python_version system;
    src = ./.;
  };
in
  out
