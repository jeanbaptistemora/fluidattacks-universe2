let
  pkgs = import ../pkgs/asserts.nix;
  inputs = [
    pkgs.tesseract
    pkgs.python37Packages.selenium
    pkgs.python37Packages.python_magic
  ];
in
  import ../../asserts/deploy/dependencies/tests.nix { inherit pkgs; inherit inputs; }
