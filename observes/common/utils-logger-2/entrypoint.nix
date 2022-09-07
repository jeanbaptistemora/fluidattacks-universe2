# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
fetchNixpkgs: let
  python_version = "python310";
  nixpkgs = fetchNixpkgs {
    rev = "97bdf4893d643e47d2bd62e9a2ec77c16ead6b9f";
    sha256 = "pOglCsO0/pvfHvVEb7PrKhnztYYNurZZKrc9YfumhJQ=";
  };
  fa-purity = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/purity";
      rev = "d87febb01c00d8a3d0f770b16cf9c4a46eeb4b15";
      ref = "refs/tags/v1.23.0";
    };
  in
    import src {
      inherit src nixpkgs;
    };
  out = import ./. {
    inherit python_version;
    nixpkgs =
      nixpkgs
      // {
        inherit fa-purity;
      };
    src = ./.;
  };
in
  out
