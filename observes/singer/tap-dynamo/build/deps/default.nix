{
  nixpkgs,
  python_version,
}: let
  python_pkgs = nixpkgs."${python_version}Packages";
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  _fa_purity = import ./fa-purity {
    inherit nixpkgs;
  };
  _fa_singer_io = import ./fa-singer-io {
    inherit system;
    nixpkgs = nixpkgs // {purity = _fa_purity;};
  };
in
  python_pkgs
  // {
    import-linter = import ./import-linter {
      inherit lib;
      click = python_pkgs.click;
      networkx = python_pkgs.networkx;
    };
    fa-purity = _fa_purity."${python_version}".pkg;
    fa-singer-io = _fa_singer_io."${python_version}".pkg;
  }
