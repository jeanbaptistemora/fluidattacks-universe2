# Provide a pkgs.stdenv.mkDerivation that has been patched with some
# boilerplate code common to all build processes we do in the repository

path: pkgs:

attrs:

pkgs.stdenv.mkDerivation (attrs // {
  __envBashLibCommon = path "/makes/utils/common/template.sh";
  __envBashLibShopts = path "/makes/utils/shopts/template.sh";
  __envStdenv = "${pkgs.stdenv}/setup";
  builder = builtins.toFile "setup-make-derivation" ''
    source $__envStdenv
    source $__envBashLibShopts
    source $__envBashLibCommon

    use_ephemeral_dir

    ${builtins.readFile attrs.builder}
  '';
})
