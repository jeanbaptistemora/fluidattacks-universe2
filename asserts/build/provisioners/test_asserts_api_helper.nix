let
  pkgs = import ../pkgs/stable.nix;
  inputs = [
    pkgs.firefox
    pkgs.python37Packages.selenium
    pkgs.python37Packages.brotli
  ];
in
  import ../dependencies/tests.nix { inherit pkgs; inherit inputs; }
