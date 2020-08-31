let
  pkgs = import ../pkgs/asserts.nix;
  inputs = [
    pkgs.unixODBC
    pkgs.python37Packages.selenium
  ];
in
  import ../../asserts/deploy/dependencies/tests.nix { inherit pkgs; inherit inputs; }
