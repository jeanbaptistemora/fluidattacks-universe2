attrs @ {
  skimsPkgs,
  ...
}:

let
  makeDerivation = import ../../../../makes/utils/make-derivation skimsPkgs;
in
  makeDerivation {
    builder = ./builder.sh;
    buildInputs = [
      skimsPkgs.gradle
      skimsPkgs.jdk11
    ];
    envJava = "${skimsPkgs.jdk11}/bin/java";
    envANTLR = skimsPkgs.fetchurl {
      url = "https://www.antlr.org/download/antlr-4.8-complete.jar";
      sha256 = "0nms976cnqyr1ndng3haxkmknpdq6xli4cpf4x4al0yr21l9v93k";
    };
    envShell = "${skimsPkgs.bash}/bin/bash";
    envSrc = ../../../../skims/static/parsers/antlr;
    name = "skims-parsers-antlr";
  }
