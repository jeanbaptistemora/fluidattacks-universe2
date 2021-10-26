{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  name = "melts-test";
  searchPaths = {
    source = [
      outputs."/melts/config-development"
      outputs."/melts/config-runtime"
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
    ];
    bin = [
      inputs.nixpkgs.gnugrep
    ];
  };
  entrypoint = ./entrypoint.sh;
}
