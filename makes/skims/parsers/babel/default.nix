attrs @ {
  pkgsSkims,
  ...
}:

let
  buildPythonRequirements = import ../../../../makes/utils/build-python-requirements pkgsSkims;
  make = import ../../../../makes/utils/make pkgsSkims;
  makeApp = import ../../../../makes/utils/make-app pkgsSkims;
in
  makeApp {
    arguments = {
      envShell = "${pkgsSkims.bash}/bin/bash";
      envSrc = ../../../../skims/static/parsers/babel;
      envNodejs = "${pkgsSkims.nodejs}/bin/node";
      envNodejsRequirements = make {
        builder = ./builder.sh;
        buildInputs = [
          pkgsSkims.nodejs
        ];
        envSrc = ../../../../skims/static/parsers/babel;
        name = "skims-parsers-babel-nodejs-requirements";
      };
    };
    name = "skims-parsers-babel";
    template = ../../../../makes/skims/parsers/babel/entrypoint.sh;
  }
