{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "skims-batch";
  searchPaths = {
    pythonPackage = [
      (projectPath "/skims/skims")
    ];
    bin = [
      inputs.nixpkgs.python38
      outputs."/melts"
      outputs."/skims"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/env"
      outputs."/utils/git"
      outputs."/skims/config-runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
