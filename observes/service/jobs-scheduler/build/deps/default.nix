{
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  # pkg_override = names: (import ./pkg_override.nix) (x: (x ? overridePythonAttrs && builtins.elem x.pname names));
  # pycheck_override = python_pkgs: (import ./pkg_override.nix) (x: (x ? name && x.name == "pytest-check-hook")) python_pkgs.pytestCheckHook;

  override_1 = python_pkgs:
    python_pkgs
    // {
      types-click = import ./click/stubs.nix lib;
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };

  # pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;
  # pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  overrides = [];
  # overrides = map pkgs_overrides [
  #   pycheck_override
  #   pytz_override
  #   requests_override
  # ];
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_pkgs = compose ([override_1] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
