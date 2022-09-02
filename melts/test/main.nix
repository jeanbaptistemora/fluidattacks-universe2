{
  makeScript,
  inputs,
  outputs,
  ...
}:
makeScript {
  name = "melts-test";
  replace = {
    __argAwsLoginDev__ = outputs."/secretsForAwsFromGitlab/dev";
  };
  searchPaths = {
    source = [
      outputs."/melts/config/development"
      outputs."/melts/config/runtime"
      outputs."/common/utils/git"
    ];
    bin = [
      inputs.nixpkgs.gnugrep
    ];
  };
  entrypoint = ./entrypoint.sh;
}
