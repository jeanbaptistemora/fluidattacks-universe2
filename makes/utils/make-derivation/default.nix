# Provide a pkgs.stdenv.mkDerivation that has been patched with some
# boilerplate code common to all build processes we do in the repository

pkgs:

attrs:

pkgs.stdenv.mkDerivation (attrs // {
  __envBashLibCommon = ../../../makes/utils/bash-lib/common.sh;
  __envBashLibShopts = ../../../makes/utils/bash-lib/shopts.sh;
  __envStdenv = "${pkgs.stdenv}/setup";
  builder = builtins.toFile "setup-make-derivation" ''
    source $__envStdenv
    source $__envBashLibShopts
    source $__envBashLibCommon

    use_ephemeral_dir

    ${builtins.readFile attrs.builder}
  '';
})
