{
  lib,
  pythonPkgs,
}:
pythonPkgs
// {
  returns = import ./returns {
    inherit lib pythonPkgs;
  };
  types-psycopg2 = import ./psycopg2/stubs.nix lib;
}
