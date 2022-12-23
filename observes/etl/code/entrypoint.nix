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
      ref = "refs/tags/v1.27.0";
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

  utils-logger."${python_version}" = let
    src = projectPath observesIndex.common.utils_logger_2.root;
  in
    import src {
      inherit python_version src;
      nixpkgs =
        nixpkgs
        // {
          inherit fa-purity;
        };
    };

  local_pkgs = {inherit arch-lint fa-purity redshift-client utils-logger;};
  out = import ./. {
    inherit python_version;
    nixpkgs = nixpkgs // local_pkgs;
    src = ./.;
  };
in
  out
