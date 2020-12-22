attrs @ {
  pkgsSkims,
  ...
}:

let
  makeApp = import ../../../makes/utils/make-app pkgsSkims;
  config = import ../../../makes/skims/config.nix pkgsSkims;
in
  makeApp {
    arguments = {
      envRuntimeBinPath = config.osRequirements.runtimeBinPath;
      envRuntimeLibPath = config.osRequirements.runtimeLibPath;
      envParserAntlr = import ../../../makes/skims/parsers/antlr {
        inherit pkgsSkims;
      };
      envParserBabel = import ../../../makes/skims/parsers/babel {
        inherit pkgsSkims;
      };
      envPython = "${pkgsSkims.python38}/bin/python";
      envPythonRequirements = config.pythonRequirements.runtime;
      envShell = "${pkgsSkims.bash}/bin/bash";
      envSrcSkimsSkims = ../../../skims/skims;
      envSrcSkimsStatic = ../../../skims/static;
      envSrcSkimsVendor = ../../../skims/vendor;
    };
    name = "skims-bin";
    template = ../../../makes/skims/bin/entrypoint.sh;
  }
