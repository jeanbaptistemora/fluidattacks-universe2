{
  fetchNixpkgs,
  projectPath,
  observesIndex,
}: let
  python_version = "python310";
  nixpkgs = fetchNixpkgs {
    rev = "97bdf4893d643e47d2bd62e9a2ec77c16ead6b9f";
    sha256 = "pOglCsO0/pvfHvVEb7PrKhnztYYNurZZKrc9YfumhJQ=";
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${python_version}" = import _utils_logger_src {
    inherit python_version;
    src = _utils_logger_src;
    legacy_pkgs = nixpkgs;
  };

  arch-lint = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/arch_lint";
      rev = "753e5bd2ed248adc92951611b09780dcedb4e0b6";
      ref = "refs/tags/v1.0.0";
    };
  in
    import src {
      inherit src nixpkgs;
    };

  fa-purity = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/purity";
      rev = "a4599c72b88495161aa57d26216a722b22ced9c6";
      ref = "refs/tags/v1.28.0";
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

  extras = {inherit arch-lint fa-purity fa-singer-io utils-logger;};
  out = import ./. {
    inherit python_version;
    nixpkgs = nixpkgs // extras;
    src = ./.;
  };
in
  out
