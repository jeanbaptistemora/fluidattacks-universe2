# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fetchNixpkgs,
  projectPath,
  observesIndex,
}: let
  python_version = "python310";
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
      rev = "fce4bf8161bd1a9d509be93eabbc80bea43b8832";
      ref = "refs/tags/v1.6.1";
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

  extras = {inherit fa-purity fa-singer-io utils-logger;};
  out = import ./. {
    inherit python_version;
    nixpkgs = nixpkgs // extras;
    src = ./.;
  };
in
  out
