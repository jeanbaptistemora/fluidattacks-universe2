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
      outputs."/skims"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/env"
      outputs."/skims/config-runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
