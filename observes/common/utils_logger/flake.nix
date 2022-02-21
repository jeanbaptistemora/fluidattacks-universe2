{
  description = "Dynamo ETLs configuration";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
  };
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      legacy_pkgs = nixpkgs.legacyPackages."${system}";
      lib = {
        buildPythonPackage = legacy_pkgs.python39.pkgs.buildPythonPackage;
        pytestCheckHook = legacy_pkgs.python39.pkgs.pytestCheckHook;
        buildEnv = legacy_pkgs.python39.buildEnv;
      };
      pythonPkgs = legacy_pkgs.python39Packages;
      src = self;
      args = {
        inherit src lib pythonPkgs;
      };
      self_pkg = import ./build/pkg/default.nix args;
      build_env = env: import ./build/env.nix (args // {
        inherit env;
      });
    in
    {
      packages."${system}" = {
        pkg = self_pkg.runtime;
        env.runtime = build_env "runtime";
        env.dev = build_env "dev";
      };
      defaultPackage."${system}" = self.packages."${system}".pkg;
    };
}
