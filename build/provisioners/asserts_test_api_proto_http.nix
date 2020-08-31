let
  pkgs = import ../pkgs/asserts.nix;
  inputs = [
    pkgs.firefox
    pkgs.python37Packages.selenium
  ];
in
  import ../../asserts/deploy/dependencies/tests.nix { inherit pkgs; inherit inputs; }
