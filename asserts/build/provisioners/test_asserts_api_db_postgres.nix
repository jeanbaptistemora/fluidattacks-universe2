let
  pkgs = import ../pkgs/stable.nix;
  inputs = [
    pkgs.unixODBC
  ];
in
  import ../dependencies/tests.nix { inherit pkgs; inherit inputs; }
