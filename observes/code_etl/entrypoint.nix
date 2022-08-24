fetchNixpkgs: projectPath: observesIndex: let
  system = "x86_64-linux";
  python_version = "python39";
  legacy_pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "fe1e3930dbc4add352035d57dcf78d52717132b5";
    ref = "refs/tags/v1.17.0";
  };
  fa-purity = import _purity_src {
    inherit system legacy_pkgs;
    src = _purity_src;
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

  _postgres_client_src = projectPath "/observes/common/postgres-client/src";
  postgres-client."${python_version}" = import _postgres_client_src {
    inherit python_version;
    src = _postgres_client_src;
    legacy_pkgs =
      legacy_pkgs
      // {
        python39Packages =
          legacy_pkgs.python39Packages
          // {
            utils-logger = utils-logger.python39.pkg;
          };
      };
  };
  local_pkgs = {inherit postgres-client fa-purity redshift-client utils-logger;};
  out = import ./. {
    pkgs = legacy_pkgs // local_pkgs;
    python_version = "python39";
    src = ./.;
  };
in
  out
