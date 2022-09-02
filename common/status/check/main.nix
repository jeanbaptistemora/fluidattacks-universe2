{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __awsLoginDev__ = outputs."/secretsForAwsFromGitlab/dev";
    __argCommonStatusSecrets__ = projectPath "/common/status/secrets.yaml";
  };
  entrypoint = ./entrypoint.sh;
  name = "common-status-check";
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.jq
    ];
    source = [
      outputs."/common/utils/sops"
    ];
  };
}
