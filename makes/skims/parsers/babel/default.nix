attrs @ {
  pkgsSkims,
  ...
}:

let
  buildPythonRequirements = import ../../../../makes/utils/build-python-requirements pkgsSkims;
  makeDerivation = import ../../../../makes/utils/make-derivation pkgsSkims;
in
  makeDerivation {
    builder = ./builder.sh;
    buildInputs = [
      pkgsSkims.nodejs
    ];
    envSrc = ../../../../skims/static/parsers/babel;
    name = "skims-parsers-babel";
  }
