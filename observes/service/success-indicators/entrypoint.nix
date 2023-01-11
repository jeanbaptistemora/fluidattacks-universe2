fetchNixpkgs: projectPath: observesIndex: let
  python_version = "python310";
  nixpkgs = fetchNixpkgs {
    rev = "97bdf4893d643e47d2bd62e9a2ec77c16ead6b9f";
    sha256 = "pOglCsO0/pvfHvVEb7PrKhnztYYNurZZKrc9YfumhJQ=";
  };

  arch-lint = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/arch_lint";
      ref = "refs/tags/v2.3.0";
      rev = "b2d79d8824dfd1b8f191777c006ab208d38352e3";
    };
  in
    import src {
      inherit src nixpkgs;
    };

  fa-purity = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/purity";
      ref = "refs/tags/v1.27.0";
      rev = "45ddbd204ab1f75180f165f50188f2e59371c26a";
    };
  in
    import src {
      inherit src nixpkgs;
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

  redshift-client = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/redshift_client";
      ref = "refs/tags/v1.2.0";
      rev = "edd6a7627196f3bce4388c3ec118313364726d9a";
    };
  in
    import src {
      inherit src;
      legacy_pkgs = nixpkgs;
      others = {
        inherit fa-purity;
      };
    };

  extras = {inherit arch-lint fa-purity redshift-client utils-logger;};
  out = import ./. {
    inherit python_version;
    nixpkgs = nixpkgs // extras;
    src = ./.;
  };
in
  out
