# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fetchNixpkgs,
  projectPath,
  observesIndex,
}: let
  python_version = "python310";
  system = "x86_64-linux";
  nixpkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${python_version}" = import _utils_logger_src {
    inherit python_version;
    src = _utils_logger_src;
    legacy_pkgs = nixpkgs;
  };

  fa-purity = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/purity";
      rev = "6dac68449852e91d2825bfab551872132c278605";
      ref = "refs/tags/v1.24.0";
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

  _legacy_purity_src = projectPath "/observes/common/purity";
  legacy-purity."${python_version}" = import _legacy_purity_src {
    inherit system;
    legacyPkgs = nixpkgs;
    src = _legacy_purity_src;
    pythonVersion = python_version;
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

  extras = {inherit fa-purity fa-singer-io legacy-purity legacy-paginator legacy-singer-io utils-logger;};
  out = import ./. {
    inherit extras;
    legacyPkgs = nixpkgs;
    pythonVersion = python_version;
    src = ./.;
  };
in
  out
