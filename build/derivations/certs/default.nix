pkgs:

pkgs.stdenv.mkDerivation rec {
  name = "certs";

  srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;

  builder = ./builder.sh;
  buildInputs = [
    pkgs.openssl
  ];
}
