let
  pkgs = import ../pkgs/stable.nix;
  inputs = [];
in
  import ../../asserts/deploy/dependencies/tests.nix { inherit pkgs; inherit inputs; }
