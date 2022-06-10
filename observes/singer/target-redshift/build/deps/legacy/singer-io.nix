{
  nixpkgs,
  projectPath,
  python_version,
  system,
}: let
  _legacy_purity_src = projectPath "/observes/common/purity";
  legacy-purity."${python_version}" = import _legacy_purity_src {
    inherit system;
    legacyPkgs = nixpkgs;
    pythonVersion = python_version;
    src = _legacy_purity_src;
  };
  src = projectPath "/observes/common/singer-io";
in
  import src {
    inherit python_version src;
    local_pkgs = {
      inherit legacy-purity;
    };
    pkgs = nixpkgs;
  }
