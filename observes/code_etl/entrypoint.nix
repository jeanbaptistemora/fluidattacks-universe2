# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
fetchNixpkgs: projectPath: observesIndex: let
  python_version = "python39";
  nixpkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  fa-purity = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/purity";
      ref = "refs/tags/v1.26.0";
    };
  in
    import src {
      inherit src nixpkgs;
    };

  redshift-client = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/redshift_client";
      ref = "refs/tags/v1.2.0";
    };
  in
    import src {
      inherit src;
      legacy_pkgs = nixpkgs;
      others = {
        inherit fa-purity;
      };
    };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${python_version}" = import _utils_logger_src {
    inherit python_version;
    legacy_pkgs = nixpkgs;
    src = _utils_logger_src;
  };

  local_pkgs = {inherit fa-purity redshift-client utils-logger;};
  out = import ./. {
    pkgs = nixpkgs // local_pkgs;
    python_version = "python39";
    src = ./.;
  };
in
  out
