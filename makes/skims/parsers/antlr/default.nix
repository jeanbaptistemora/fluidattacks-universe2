let
  make = import ../../../../makes/utils/make pkgs;
  pkgs = import ../../../../makes/skims/pkgs.nix;
in
  make {
    builder = ./builder.sh;
    buildInputs = [
      pkgs.gradle
      pkgs.jdk11
    ];
    envANTLR = pkgs.fetchurl {
      url = "https://www.antlr.org/download/antlr-4.8-complete.jar";
      sha256 = "0nms976cnqyr1ndng3haxkmknpdq6xli4cpf4x4al0yr21l9v93k";
    };
    envSrc = ../../../../skims/static/parsers/antlr;
    name = "skims-parsers-antlr";
  }
