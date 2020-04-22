let
  pkgs = import ../build/pkgs/stable.nix;
in
pkgs.python37Packages.buildPythonApplication rec {
  pname = "fluidattacks";
  version = "2020";
  src = ./.;
  pyPkgFluidattacks = import ./default.nix pkgs;
  doCheck = false;
  installPhase = ./pip-install-hook.sh;
  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib64:$LD_LIBRARY_PATH";
}
