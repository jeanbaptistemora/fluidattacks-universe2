{
  fetchNixpkgs,
  projectPath,
  observesIndex,
}: let
  system = "x86_64-linux";
  python_version = "python38";
  nixpkgs = fetchNixpkgs {
    rev = "97bdf4893d643e47d2bd62e9a2ec77c16ead6b9f";
    sha256 = "pOglCsO0/pvfHvVEb7PrKhnztYYNurZZKrc9YfumhJQ=";
  };
  utils-logger."${python_version}" = let
    src = projectPath observesIndex.common.utils_logger.root;
  in
    import src {
      inherit python_version src;
      legacy_pkgs = nixpkgs;
    };
  out = import ./. {
    inherit python_version system;
    nixpkgs =
      nixpkgs
      // {
        inherit utils-logger;
      };
    src = ./.;
  };
in
  out
