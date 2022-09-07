# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
fetchNixpkgs: projectPath: observesIndex: let
  system = "x86_64-linux";
  python_version = "python310";
  pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${python_version}" = import _utils_logger_src {
    inherit python_version;
    src = _utils_logger_src;
    legacy_pkgs = pkgs;
  };

  _fa_purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "ced4246ae36b30a7c0be99b8f15eae60cc403ca3";
    ref = "refs/tags/v1.18.1";
  };
  fa-purity = import _fa_purity_src {
    inherit system;
    legacy_pkgs = pkgs;
    src = _fa_purity_src;
  };

  _redshift_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    rev = "8fef869f11bb947e4e4887b2df9f27650b35910f";
    ref = "refs/tags/v0.7.0";
  };
  redshift-client = import _redshift_src {
    inherit system;
    legacy_pkgs = pkgs;
    src = _redshift_src;
    others = {
      inherit fa-purity;
    };
  };

  local_pkgs = {inherit fa-purity redshift-client utils-logger;};
  out = import ./. {
    inherit local_pkgs pkgs python_version;
    src = ./.;
  };
in
  out
