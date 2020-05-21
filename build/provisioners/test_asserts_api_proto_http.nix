let
  pkgs = import ../pkgs/stable.nix;
  inputs = [
    pkgs.firefox
    pkgs.python37Packages.selenium
  ];
in
  import ../dependencies/tests.nix { inherit pkgs; inherit inputs; }
