# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
fetchNixpkgs: projectPath: let
  python_version = "python38";
  system = "x86_64-linux";
  legacyPkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _legacy_purity_src = projectPath "/observes/common/purity";
  legacy-purity."${python_version}" = import _legacy_purity_src {
    inherit system;
    legacyPkgs = pkgs;
    pythonVersion = python_version;
    src = _legacy_purity_src;
  };

  local_pkgs = {
    inherit legacy-purity;
  };
  out = import ./. {
    inherit local_pkgs python_version;
    pkgs = legacyPkgs;
    src = ./.;
  };
in
  out
