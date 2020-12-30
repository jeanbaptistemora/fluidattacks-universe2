attrs @ {
  pkgsSkims,
  ...
}:

let
  makeDerivation = import ../../../../makes/utils/make-derivation pkgsSkims;
in
  makeDerivation {
    builder = ./builder.sh;
    buildInputs = [
      pkgsSkims.gradle
      pkgsSkims.jdk11
    ];
    envJava = "${pkgsSkims.jdk11}/bin/java";
    envANTLR = pkgsSkims.fetchurl {
      url = "https://www.antlr.org/download/antlr-4.8-complete.jar";
      sha256 = "0nms976cnqyr1ndng3haxkmknpdq6xli4cpf4x4al0yr21l9v93k";
    };
    envShell = "${pkgsSkims.bash}/bin/bash";
    envSrc = ../../../../skims/static/parsers/antlr;
    name = "skims-parsers-antlr";
  }
