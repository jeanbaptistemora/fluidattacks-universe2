let
  pkgs = import ../pkgs/stable.nix;
  inputs = [
    pkgs.tesseract
    pkgs.python37Packages.selenium
    pkgs.python37Packages.python_magic
  ];
in
  import ../dependencies/tests.nix { inherit pkgs; inherit inputs; }
