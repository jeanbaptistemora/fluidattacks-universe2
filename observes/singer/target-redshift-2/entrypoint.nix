# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
fetchNixpkgs: projectPath: observesIndex: let
  python_version = "python310";
  nixpkgs = fetchNixpkgs {
    rev = "97bdf4893d643e47d2bd62e9a2ec77c16ead6b9f";
    sha256 = "pOglCsO0/pvfHvVEb7PrKhnztYYNurZZKrc9YfumhJQ=";
  };

  arch-lint = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/arch_lint";
      rev = "753e5bd2ed248adc92951611b09780dcedb4e0b6";
      ref = "refs/tags/v1.0.0";
    };
  in
    import src {
      inherit src nixpkgs;
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

  fa-singer-io = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/singer_io";
      rev = "d35487441ba37e2a98dca789741407231576e481";
      ref = "refs/tags/v1.4.0";
    };
  in
    import src {
      inherit src;
      nixpkgs =
        nixpkgs
        // {
          purity = fa-purity;
        };
    };

  redshift-client = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/redshift_client";
      rev = "1644320c6877376cd80900d8d3d7e4457fdb54e9";
      ref = "refs/tags/v1.1.1";
    };
  in
    import src {
      inherit src;
      legacy_pkgs = nixpkgs;
      others = {
        inherit fa-purity;
      };
    };

  utils-logger."${python_version}" = let
    src = projectPath observesIndex.common.utils_logger_2.root;
  in
    import src {
      inherit python_version src;
      nixpkgs =
        nixpkgs
        // {
          inherit fa-purity;
        };
    };

  out = import ./. {
    inherit python_version;
    nixpkgs =
      nixpkgs
      // {
        inherit arch-lint fa-purity fa-singer-io redshift-client utils-logger;
      };
    src = ./.;
  };
in
  out
