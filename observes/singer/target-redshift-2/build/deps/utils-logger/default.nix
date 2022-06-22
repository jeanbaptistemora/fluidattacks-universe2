{
  observesIndex,
  nixpkgs,
  projectPath,
  python_version,
}: let
  src = projectPath observesIndex.common.utils_logger.root;
in
  import src {
    inherit python_version src;
    legacy_pkgs = nixpkgs;
  }
