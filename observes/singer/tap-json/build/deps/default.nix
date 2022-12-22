{
  nixpkgs,
  python_version,
  no_test,
}: let
  utils = import ./override_utils.nix;
  pkgs = let
    no_test_pkgs = nixpkgs.extend (_: super: {
      "${python_version}" = let
        packageOverrides = _: utils.apply_python_pkgs_override utils.no_check_override;
      in
        super."${python_version}".override {inherit packageOverrides;};
    });
  in
    if no_test
    then no_test_pkgs
    else nixpkgs;
  lib = {
    buildEnv = pkgs."${python_version}".buildEnv.override;
    buildPythonPackage = pkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = pkgs.python3Packages.fetchPypi;
  };

  override_1 = python_pkgs:
    python_pkgs
    // {
      arch-lint = pkgs.arch-lint."${python_version}".pkg;
      fa-purity = pkgs.fa-purity."${python_version}".pkg;
      types-python-dateutil = import ./types-python-dateutil.nix {inherit lib;};
      utils-logger = pkgs.utils-logger."${python_version}".pkg;
    };
  final_pkgs = utils.compose [override_1] (pkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
