{
  makeScript,
  outputs,
  inputs,
  ...
}:
makeScript {
  replace = {
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromGitlab/prodObserves";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      outputs."/melts"
    ];
    source = [
      outputs."/common/utils/git"
    ];
  };
  name = "observes-etl-code-mirror";
  entrypoint = ./entrypoint.sh;
}
