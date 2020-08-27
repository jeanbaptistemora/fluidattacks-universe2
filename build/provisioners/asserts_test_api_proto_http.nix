let
  pkgs = import ../pkgs/stable.nix;
  inputs = [
    pkgs.firefox
    pkgs.python37Packages.selenium
  ];
in
  import ../../asserts/deploy/dependencies/tests.nix { inherit pkgs; inherit inputs; }
