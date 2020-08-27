let
  pkgs = import ../pkgs/stable.nix;
  inputs = [
    pkgs.unixODBC
  ];
in
  import ../../asserts/deploy/dependencies/tests.nix { inherit pkgs; inherit inputs; }
