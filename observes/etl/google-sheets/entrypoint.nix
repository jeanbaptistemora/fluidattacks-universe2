fetchNixpkgs: projectPath: observesIndex: let
  python_version = "python311";
  nixpkgs = fetchNixpkgs {
    rev = "97bdf4893d643e47d2bd62e9a2ec77c16ead6b9f";
    sha256 = "pOglCsO0/pvfHvVEb7PrKhnztYYNurZZKrc9YfumhJQ=";
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

  out = import ./build {
    inherit python_version;
    nixpkgs =
      nixpkgs
      // {
        inherit utils-logger;
      };
    src = ./.;
  };
in
  out
