attrs @ {
  pkgsSkims,
  ...
}:

let
  buildPythonRequirements = import ../../../../makes/utils/build-python-requirements pkgsSkims;
  make = import ../../../../makes/utils/make pkgsSkims;
  makeApp = import ../../../../makes/utils/make-app pkgsSkims;
in
  make {
    builder = ./builder.sh;
    buildInputs = [
      pkgsSkims.nodejs
    ];
    envSrc = ../../../../skims/static/parsers/babel;
    name = "skims-parsers-babel";
  }
