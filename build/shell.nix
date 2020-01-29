let
  pkgs = import ./pkgs.nix { };
  main = import ./main.nix;

  osPackages = with pkgs; [
    docker
    gnupg
  ];

  pythonPackages = with main._pythonPackages; [
    twine
  ];

  propagatedBuildInputs = with main; [
    pyPkgFluidassertsBasic.buildInputs
    pyPkgGroupTest.buildInputs
    pyPkgMandrill.buildInputs
    pyPkgGitPython.buildInputs
  ];
in

with main;

pkgs.stdenv.mkDerivation rec {
  name = "shell";
  inherit genericDirs genericShellOptions;
  inherit pyPkgFluidassertsBasic;
  inherit pyPkgGroupTest;
  inherit pyPkgMandrill;
  inherit pyPkgGitPython;
  buildInputs = osPackages ++ pythonPackages ++ propagatedBuildInputs;
}
