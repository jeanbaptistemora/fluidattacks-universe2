# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
fetchNixpkgs: projectPath: observesIndex: let
  system = "x86_64-linux";
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

  _legacy_purity_src = projectPath "/observes/common/purity";
  legacy-purity."${python_version}" = import _legacy_purity_src {
    inherit system;
    legacyPkgs = nixpkgs;
    pythonVersion = python_version;
    src = _legacy_purity_src;
  };

  _legacy_paginator_src = projectPath "/observes/common/paginator";
  legacy-paginator."${python_version}" = import _legacy_paginator_src {
    inherit python_version;
    local_pkgs = {
      inherit legacy-purity;
    };
    pkgs = nixpkgs;
    src = _legacy_paginator_src;
  };

  _legacy_singer_io = projectPath "/observes/common/singer-io";
  legacy-singer-io."${python_version}" = import _legacy_singer_io {
    inherit python_version;
    local_pkgs = {
      inherit legacy-purity;
    };
    pkgs = nixpkgs;
    src = _legacy_singer_io;
  };

  local_pkgs = {inherit fa-purity fa-singer-io legacy-paginator legacy-singer-io utils-logger;};
  out = import ./. {
    inherit python_version;
    nixpkgs = nixpkgs // local_pkgs;
    src = ./.;
  };
in
  out
