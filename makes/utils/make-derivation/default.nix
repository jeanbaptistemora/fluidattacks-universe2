# Provide a pkgs.stdenv.mkDerivation that has been patched with some
# boilerplate code common to all build processes we do in the repository

pkgs:

attrs:

pkgs.stdenv.mkDerivation (attrs // {
  __envBashLibShopts = ../../../makes/utils/bash-lib/shopts.sh;
  __envBashLibDrv = ../../../makes/utils/bash-lib/drv.sh;
  __envStdenv = "${pkgs.stdenv}/setup";
  makeDerivation = builtins.toFile "setup-make-derivation" ''
    source $__envStdenv
    source $__envBashLibShopts
    source $__envBashLibDrv

    initialize
  '';
})
