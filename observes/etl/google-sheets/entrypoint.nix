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
  utils-logger-src = projectPath observesIndex.common.utils_logger_2.root;
  nix-filter = let
    src = builtins.fetchGit {
      url = "https://github.com/numtide/nix-filter";
      rev = "fc282c5478e4141842f9644c239a41cfe9586732";
    };
  in
    import src;

  # bins
  tap-google-sheets = let
    root = projectPath observesIndex.tap.google_sheets.root;
    pkg = import "${root}/entrypoint.nix" {
      inherit fetchNixpkgs;
    };
  in
    pkg.env.bin;

  out = import ./build {
    inherit python_version;
    nixpkgs =
      nixpkgs
      // {
        inherit tap-google-sheets utils-logger-src;
      };
    src = nix-filter {
      root = ./.;
      include = [
        "google_sheets_etl"
        "tests"
        "pyproject.toml"
        "mypy.ini"
      ];
    };
  };
in
  out
