attrs @ {
  pkgsSkims,
  ...
}:

let
  config = import ../../../makes/skims/config.nix attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint pkgsSkims;
in
  makeEntrypoint {
    arguments = {
      envContextFile = config.contextFile;
      envRuntimeBinPath = config.osRequirements.runtimeBinPath;
      envRuntimeLibPath = config.osRequirements.runtimeLibPath;
      envPython = "${pkgsSkims.python38}/bin/python";
      envPythonRequirements = config.pythonRequirements.runtime;
      envShell = "${pkgsSkims.bash}/bin/bash";
      envSrcSkimsSkims = ../../../skims/skims;
    };
    name = "skims-bin";
    template = ../../../makes/skims/bin/entrypoint.sh;
  }
