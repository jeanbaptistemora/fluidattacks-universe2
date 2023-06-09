{
  makeScript,
  inputs,
  outputs,
  ...
}:
makeScript {
  name = "melts-test";
  searchPaths = {
    source = [
      outputs."/melts/config/development"
      outputs."/melts/config/runtime"
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
    ];
    bin = [
      inputs.nixpkgs.gnugrep
    ];
  };
  entrypoint = ./entrypoint.sh;
}
