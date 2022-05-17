{
  lib,
  local_pkgs,
  pkgs,
  python_version,
}: let
  python_pkgs = pkgs."${python_version}Packages";
in
  python_pkgs
  // {
    types-click = import ./click/stubs.nix lib;
    types-psycopg2 = import ./psycopg2/stubs.nix lib;
    import-linter = import ./import-linter {
      inherit lib python_pkgs;
    };
    utils-logger = local_pkgs.utils-logger."${python_version}".pkg;
  }
