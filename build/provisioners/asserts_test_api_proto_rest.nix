let
  pkgs = import ../pkgs/asserts.nix;
  inputs = [
    pkgs.python37Packages.selenium
    pkgs.python37Packages.brotli
  ];
in
  import ../../asserts/deploy/dependencies/tests.nix { inherit pkgs; inherit inputs; }
