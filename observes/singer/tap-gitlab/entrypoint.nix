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

  _fa_singer_io_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/singer_io";
    rev = "e5e1f74f6585f4a0f2ab1a7be31df907694a9d7d";
    ref = "refs/tags/v1.3.0";
  };
  fa-singer-io = import _fa_singer_io_src {
    inherit system;
    legacyPkgs = legacy_pkgs;
    src = _fa_singer_io_src;
    purity = fa-purity;
  };

  _redshift_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    rev = "8fef869f11bb947e4e4887b2df9f27650b35910f";
    ref = "refs/tags/v0.7.0";
  };
  redshift-client = import _redshift_src {
    inherit system legacy_pkgs;
    src = _redshift_src;
    others = {
      inherit fa-purity;
    };
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${python_version}" = import _utils_logger_src {
    inherit legacy_pkgs python_version;
    src = _utils_logger_src;
  };

  _legacy_postgres_client_src = projectPath "/observes/common/postgres-client/src";
  legacy-postgres-client."${python_version}" = import _legacy_postgres_client_src {
    inherit python_version;
    src = _legacy_postgres_client_src;
    legacy_pkgs =
      legacy_pkgs
      // {
        "${python_version}Packages" =
          legacy_pkgs."${python_version}Packages"
          // {
            utils-logger = utils-logger."${python_version}".pkg;
          };
      };
  };

  _legacy_purity_src = projectPath "/observes/common/purity";
  legacy-purity."${python_version}" = import _legacy_purity_src {
    inherit system;
    legacyPkgs = legacy_pkgs;
    pythonVersion = python_version;
    src = _legacy_purity_src;
  };

  _legacy_paginator_src = projectPath "/observes/common/paginator";
  legacy-paginator."${python_version}" = import _legacy_paginator_src {
    inherit python_version;
    local_pkgs = {
      inherit legacy-purity;
    };
    pkgs = legacy_pkgs;
    src = _legacy_paginator_src;
  };

  _legacy_singer_io = projectPath "/observes/common/singer-io";
  legacy-singer-io."${python_version}" = import _legacy_singer_io {
    inherit python_version;
    local_pkgs = {
      inherit legacy-purity;
    };
    pkgs = legacy_pkgs;
    src = _legacy_singer_io;
  };

  local_pkgs = {inherit fa-purity fa-singer-io legacy-paginator legacy-postgres-client legacy-singer-io redshift-client utils-logger;};
  out = import ./. {
    inherit python_version;
    pkgs = legacy_pkgs // local_pkgs;
    src = ./.;
  };
in
  out
