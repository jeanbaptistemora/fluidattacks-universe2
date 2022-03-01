{
  description = "DB migration utils";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    nix_filter.url = "github:numtide/nix-filter";
    redshift_client.url = "gitlab:dmurciaatfluid/redshift_client";
  };
  outputs = { self, nixpkgs, nix_filter, redshift_client }:
    let
      system = "x86_64-linux";
      metadata = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).tool.poetry;
      legacy_pkgs = nixpkgs.legacyPackages."${system}";
      lib = {
        buildPythonPackage = legacy_pkgs.python39.pkgs.buildPythonPackage;
        fetchPypi = legacy_pkgs.python3Packages.fetchPypi;
      };
      pythonPkgs = legacy_pkgs.python39Packages // {
        redshift-client = redshift_client.defaultPackage."${system}";
      };
      path_filter = nix_filter.outputs.lib;
      src = path_filter {
        root = self;
        include = [
          "pyproject.toml"
          (path_filter.inDirectory metadata.name)
        ];
      };
      self_pkgs = import ./build/pkg {
        inherit src lib metadata pythonPkgs;
      };
      build_env = pkg: legacy_pkgs.python39.buildEnv.override {
        extraLibs = [ pkg ];
        ignoreCollisions = false;
      };
    in
    {
      packages."${system}" = {
        env.runtime = build_env self_pkgs.runtime;
        env.dev = build_env self_pkgs.dev;
        pkg = self_pkgs.runtime;
      };
      defaultPackage."${system}" = self.packages."${system}".pkg;
    };
}

