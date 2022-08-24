fetchNixpkgs: projectPath: observesIndex: let
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

  _supported_versions = ["python38" "python39" "python310"];
  _build_utils_logger = let
    src = projectPath observesIndex.common.utils_logger_2.root;
  in
    python_version:
      import src {
        inherit python_version src;
        nixpkgs =
          nixpkgs
          // {
            inherit fa-purity;
          };
      };
  utils-logger = builtins.listToAttrs (map (name: {
      inherit name;
      value = _build_utils_logger name;
    })
    _supported_versions);
  extras = {inherit fa-purity utils-logger;};
  pkg = import ./. {
    nixpkgs = nixpkgs // extras;
    src = ./.;
  };
in
  pkg
