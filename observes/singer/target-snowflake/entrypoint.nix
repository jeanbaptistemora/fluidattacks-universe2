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

  path_filter = let
    src = builtins.fetchGit {
      url = "https://github.com/numtide/nix-filter";
      rev = "3b821578685d661a10b563cba30b1861eec05748";
    };
  in
    import src;

  src = path_filter {
    root = ./.;
    include = [
      "mypy.ini"
      "pyproject.toml"
      (path_filter.inDirectory "target_snowflake")
      (path_filter.inDirectory "tests")
    ];
  };

  out = import ./. {
    inherit src python_version;
    nixpkgs =
      nixpkgs
      // {
        inherit arch-lint fa-purity fa-singer-io utils-logger;
      };
  };
in
  out
