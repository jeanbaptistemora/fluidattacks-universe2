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
  arch-lint = import ./arch_lint.nix {inherit nixpkgs;};
  fa-purity = import ./fa_purity.nix {inherit nixpkgs;};
  utils-logger = import ./utils_logger.nix {
    inherit nixpkgs fa-purity python_version;
    src = nixpkgs.utils-logger-src;
  };
  override_1 = python_pkgs:
    python_pkgs
    // {
      inherit utils-logger;
      arch-lint = arch-lint."${python_version}".pkg;
      fa-purity = fa-purity."${python_version}".pkg;
    };
  final_pkgs = utils.compose [override_1] (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
