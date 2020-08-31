let
  pkgs = import ../pkgs/asserts.nix;
  inputs = [
    pkgs.unixODBC
  ];
in
  import ../../asserts/deploy/dependencies/tests.nix { inherit pkgs; inherit inputs; }
