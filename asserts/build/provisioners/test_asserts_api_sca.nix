let
  pkgs = import ../pkgs/stable.nix;
  inputs = [];
in
  import ../dependencies/tests.nix { inherit pkgs; inherit inputs; }
