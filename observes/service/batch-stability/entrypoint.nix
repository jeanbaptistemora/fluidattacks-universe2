fetchNixpkgs: projectPath: observesIndex: let
  system = "x86_64-linux";
  legacy_pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "refs/tags/v1.17.0";
  };
  fa-purity = import _purity_src {
    inherit system legacy_pkgs;
    src = _purity_src;
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  _supported_versions = ["python38" "python39" "python310"];
  _build_utils-logger = python_version:
    import _utils_logger_src {
      inherit legacy_pkgs python_version;
      src = _utils_logger_src;
    };
  utils-logger = builtins.listToAttrs (map (name: {
      inherit name;
      value = _build_utils-logger name;
    })
    _supported_versions);
  extras = {inherit fa-purity utils-logger;};
  pkg = import ./. {
    inherit legacy_pkgs extras;
    src = ./.;
  };
in
  pkg
