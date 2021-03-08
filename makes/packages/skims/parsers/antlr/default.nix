{ fetchurl
, makeDerivation
, path
, nixpkgs
, ...
}:
let
  envANTLR = fetchurl {
    sha256 = "0nms976cnqyr1ndng3haxkmknpdq6xli4cpf4x4al0yr21l9v93k";
    url = "https://www.antlr.org/download/antlr-4.8-complete.jar";
  };
in
makeDerivation {
  arguments = {
    inherit envANTLR;
    envSrc = path "/skims/static/parsers/antlr";
  };
  builder = path "/makes/packages/skims/parsers/antlr/builder.sh";
  name = "skims-parsers-antlr";
  searchPaths = {
    envClassPaths = [ envANTLR ];
    envPaths = [
      nixpkgs.bash
      nixpkgs.openjdk_headless
      nixpkgs.gradle
    ];
  };
}
