fetchNixpkgs: projectPath: observesIndex: let
  python_version = "python310";
  system = "x86_64-linux";
  legacyPkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${python_version}" = import _utils_logger_src {
    inherit python_version;
    src = _utils_logger_src;
    legacy_pkgs = legacyPkgs;
  };

  _purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "refs/tags/v1.17.0";
  };
  purity = import _purity_src {
    inherit system;
    legacy_pkgs = legacyPkgs;
    src = _purity_src;
  };

  _singer_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/singer_io";
    ref = "refs/tags/v1.1.0";
  };
  singer-io = import _singer_src {
    inherit system purity legacyPkgs;
    src = _singer_src;
  };

  _legacy_purity_src = projectPath "/observes/common/purity";
  legacy-purity."${python_version}" = import _legacy_purity_src {
    inherit legacyPkgs system;
    src = _legacy_purity_src;
    pythonVersion = python_version;
  };

  _legacy_paginator_src = projectPath "/observes/common/paginator";
  legacy-paginator."${python_version}" = import _legacy_paginator_src {
    inherit python_version;
    local_pkgs = {
      inherit legacy-purity;
    };
    pkgs = legacyPkgs;
    src = _legacy_paginator_src;
  };

  _legacy_singer_io = projectPath "/observes/common/singer-io";
  legacy-singer-io."${python_version}" = import _legacy_singer_io {
    inherit python_version;
    local_pkgs = {
      inherit legacy-purity;
    };
    pkgs = legacyPkgs;
    src = _legacy_singer_io;
  };

  extras = {inherit purity singer-io legacy-purity legacy-paginator legacy-singer-io utils-logger;};
  out = import ./. {
    inherit legacyPkgs extras;
    pythonVersion = python_version;
    src = ./.;
  };
in
  out
