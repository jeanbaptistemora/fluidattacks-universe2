{
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };

  override_1 = python_pkgs:
    python_pkgs
    // {
      import-linter = import ./import-linter {
        inherit lib;
        click = python_pkgs.click;
        networkx = python_pkgs.networkx;
      };
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
      mypy-boto3-batch = import ./boto3/batch-stubs.nix lib python_pkgs;
      types-boto3 = import ./boto3/stubs.nix lib python_pkgs;
      types-click = import ./click/stubs.nix lib;
    };

  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  overrides = map pkgs_overrides [];
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_pkgs = compose ([override_1] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
