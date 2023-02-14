{
  nixpkgs,
  python_version,
}: let
  utils = import ./override_utils.nix;
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  arch-lint = (import ./arch_lint.nix)."${python_version}".pkg;
  fa-purity = (import ./fa_purity.nix)."${python_version}".pkg;
  override_1 = python_pkgs:
    python_pkgs
    // {
      inherit arch-lint fa-purity;
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };
  final_pkgs = utils.compose [override_1] (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
