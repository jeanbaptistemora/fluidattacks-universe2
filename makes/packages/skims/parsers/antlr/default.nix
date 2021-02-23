{ path
, skimsPkgs
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  arguments = {
    envANTLR = skimsPkgs.fetchurl {
      sha256 = "0nms976cnqyr1ndng3haxkmknpdq6xli4cpf4x4al0yr21l9v93k";
      url = "https://www.antlr.org/download/antlr-4.8-complete.jar";
    };
    envJava = "${skimsPkgs.openjdk_headless}/bin/java";
    envJavac = "${skimsPkgs.openjdk_headless}/bin/javac";
    envShell = "${skimsPkgs.bash}/bin/bash";
    envSrc = path "/skims/static/parsers/antlr";
  };
  builder = path "/makes/packages/skims/parsers/antlr/builder.sh";
  name = "skims-parsers-antlr";
  searchPaths = {
    envPaths = [ skimsPkgs.gradle ];
  };
}
