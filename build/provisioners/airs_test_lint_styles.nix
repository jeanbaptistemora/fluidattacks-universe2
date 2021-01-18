let
  pkgs = import ../pkgs/airs.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.nodejs
        pkgs.autoconf
        pkgs.libtool
        pkgs.automake
        pkgs.nasm
        pkgs.dpkg
        pkgs.pkgconfig
        pkgs.libpng
        pkgs.gcc
      ];
    })
  )
