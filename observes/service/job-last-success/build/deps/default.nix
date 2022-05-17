{
  lib,
  python_pkgs,
}:
python_pkgs
// {
  types-click = import ./click/stubs.nix lib;
  types-psycopg2 = import ./psycopg2/stubs.nix lib;
  import-linter = import ./import-linter {
    inherit lib python_pkgs;
  };
}
