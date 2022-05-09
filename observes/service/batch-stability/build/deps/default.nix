{
  lib,
  python_pkgs,
}:
python_pkgs
// {
  import-linter = import ./import-linter {
    inherit lib;
    click = python_pkgs.click;
    networkx = python_pkgs.networkx;
  };
  types-click = import ./click/stubs.nix lib;
}
