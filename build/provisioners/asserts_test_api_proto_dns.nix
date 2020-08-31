let
  pkgs = import ../pkgs/asserts.nix;
  inputs = [];
in
  import ../../asserts/deploy/dependencies/tests.nix { inherit pkgs; inherit inputs; }
