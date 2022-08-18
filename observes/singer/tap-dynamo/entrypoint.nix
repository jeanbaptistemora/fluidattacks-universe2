{
  fetchNixpkgs,
  projectPath,
  observesIndex,
}: let
  python_version = "python38";
  nixpkgs = fetchNixpkgs {
    rev = "97bdf4893d643e47d2bd62e9a2ec77c16ead6b9f";
    sha256 = "pOglCsO0/pvfHvVEb7PrKhnztYYNurZZKrc9YfumhJQ=";
  };

  arch-lint = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/arch_lint";
      ref = "refs/tags/v1.0.0";
    };
  in
    import src {
      inherit src nixpkgs;
    };

  utils-logger."${python_version}" = let
    src = projectPath observesIndex.common.utils_logger.root;
  in
    import src {
      inherit python_version src;
      legacy_pkgs = nixpkgs;
    };
  out = import ./. {
    inherit python_version;
    nixpkgs =
      nixpkgs
      // {
        inherit arch-lint utils-logger;
      };
    src = ./.;
  };
in
  out
