{ fetchurl
, path
, nixpkgs
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixpkgs;
in
makeDerivation {
  arguments = {
    envANTLR = fetchurl {
      sha256 = "0nms976cnqyr1ndng3haxkmknpdq6xli4cpf4x4al0yr21l9v93k";
      url = "https://www.antlr.org/download/antlr-4.8-complete.jar";
    };
    envJava = "${nixpkgs.openjdk_headless}/bin/java";
    envJavac = "${nixpkgs.openjdk_headless}/bin/javac";
    envShell = "${nixpkgs.bash}/bin/bash";
    envSrc = path "/skims/static/parsers/antlr";
  };
  builder = path "/makes/packages/skims/parsers/antlr/builder.sh";
  name = "skims-parsers-antlr";
  searchPaths = {
    envPaths = [ nixpkgs.gradle ];
  };
}
