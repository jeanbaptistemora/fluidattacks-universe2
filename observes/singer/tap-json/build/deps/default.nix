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
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
    };

  compose = functions: val: builtins.foldl' (x: f: f x) val functions;
  final_pkgs = compose [override_1] (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
