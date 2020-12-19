# Provide a pkgs.stdenv.mkDerivation that has been patched with some
# boilerplate code common to all build processes we do in the repository

pkgs:

attrs:

pkgs.stdenv.mkDerivation (attrs // {
  __envStdenv = "${pkgs.stdenv}/setup";
  __envUtils = ../../../makes/utils/make/utils.sh;
  makeSetup = builtins.toFile "setup" ''
    source $__envStdenv
    source $__envUtils

    initialize
  '';
})
