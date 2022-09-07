# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
fetchNixpkgs: projectPath: observesIndex: let
  system = "x86_64-linux";
  python_version = "python310";
  legacy_pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _fa_purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "ced4246ae36b30a7c0be99b8f15eae60cc403ca3";
    ref = "refs/tags/v1.18.1";
  };
  fa-purity = import _fa_purity_src {
    inherit system legacy_pkgs;
    src = _fa_purity_src;
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${python_version}" = import _utils_logger_src {
    inherit legacy_pkgs python_version;
    src = _utils_logger_src;
  };

  local_pkgs = {inherit fa-purity utils-logger;};
  out = import ./. {
    inherit python_version;
    pkgs = legacy_pkgs // local_pkgs;
    src = ./.;
  };
in
  out
