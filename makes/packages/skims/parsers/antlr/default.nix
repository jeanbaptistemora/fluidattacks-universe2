{ path
, skimsPkgs
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/skims/parsers/antlr/builder.sh";
  buildInputs = [
    skimsPkgs.gradle
  ];
  envANTLR = skimsPkgs.fetchurl {
    sha256 = "0nms976cnqyr1ndng3haxkmknpdq6xli4cpf4x4al0yr21l9v93k";
    url = "https://www.antlr.org/download/antlr-4.8-complete.jar";
  };
  envJava = "${skimsPkgs.openjdk_headless}/bin/java";
  envJavac = "${skimsPkgs.openjdk_headless}/bin/javac";
  envShell = "${skimsPkgs.bash}/bin/bash";
  envSrc = path "/skims/static/parsers/antlr";
  name = "skims-parsers-antlr";
}
