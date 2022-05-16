fetchNixpkgs: projectPath: observesIndex: let
  pythonVersion = "python310";
  system = "x86_64-linux";
  localLib = {
    utils-logger = projectPath observesIndex.common.utils_logger.root;
    legacy-paginator = projectPath "/observes/common/paginator";
    legacy-purity = projectPath "/observes/common/purity";
    legacy-singer-io = projectPath "/observes/common/singer-io";
  };
  legacyPkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${pythonVersion}" = import _utils_logger_src {
    src = _utils_logger_src;
    legacy_pkgs = legacyPkgs;
    python_version = pythonVersion;
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
  legacy-purity."${pythonVersion}" = import _legacy_purity_src {
    src = _legacy_purity_src;
    inherit legacyPkgs pythonVersion system;
  };

  _legacy_paginator_src = projectPath "/observes/common/paginator";
  legacy-paginator."${pythonVersion}" = import _legacy_paginator_src {
    local_pkgs = {
      inherit legacy-purity;
    };
    pkgs = legacyPkgs;
    python_version = pythonVersion;
    src = _legacy_paginator_src;
  };

  _legacy_singer_io = projectPath "/observes/common/singer-io";
  legacy-singer-io."${pythonVersion}" = import _legacy_singer_io {
    src = _legacy_singer_io;
    inherit legacyPkgs pythonVersion localLib system;
  };

  extras = {inherit purity singer-io legacy-purity legacy-paginator legacy-singer-io utils-logger;};
  out = import ./. {
    inherit legacyPkgs extras pythonVersion;
    src = ./.;
  };
in
  out
