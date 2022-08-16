fetchNixpkgs: projectPath: observesIndex: let
  system = "x86_64-linux";
  python_version = "python310";
  nixpkgs = fetchNixpkgs {
    rev = "97bdf4893d643e47d2bd62e9a2ec77c16ead6b9f";
    sha256 = "pOglCsO0/pvfHvVEb7PrKhnztYYNurZZKrc9YfumhJQ=";
  };

  fa-purity = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/purity";
      ref = "refs/tags/v1.23.0";
    };
  in
    import src {
      inherit src nixpkgs;
    };

  fa-singer-io = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/singer_io";
      ref = "main";
      rev = "5a9421e3323e4e8b701fa702b8157139298cf43f";
    };
  in
    import src {
      inherit src system;
      purity = fa-purity;
      legacyPkgs = nixpkgs;
    };

  redshift-client = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/redshift_client";
      ref = "refs/tags/v0.9.2";
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

  out = import ./. {
    inherit python_version;
    nixpkgs =
      nixpkgs
      // {
        inherit fa-purity fa-singer-io redshift-client utils-logger;
      };
    src = ./.;
  };
in
  out
