{
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  # overrides
  pkg_override = names: (import ./pkg_override.nix) (x: (x ? overridePythonAttrs && builtins.elem x.pname names));
  pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  overrides = map pkgs_overrides [
    pytz_override
  ];
  # layers
  layer_1 = python_pkgs:
    python_pkgs
    // {
      pytz = import ./pytz {inherit lib python_pkgs;};
      types-python-dateutil = import ./dateutil/stubs.nix lib;
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      fa-singer-io = nixpkgs.fa-singer-io."${python_version}".pkg;
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };
  # integrate all
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_nixpkgs = compose ([layer_1] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_nixpkgs;
}
