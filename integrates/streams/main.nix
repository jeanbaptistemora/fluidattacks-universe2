{
  inputs,
  libGit,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "integrates-streams";
  replace = {
    __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
    __argSecretsProd__ = projectPath "/integrates/secrets/production.yaml";
    __argSrc__ = projectPath "/integrates/streams/src";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli2
      # https://github.com/FasterXML/jackson-databind#jdk
      # https://github.com/aws/aws-sdk-java/issues/2795#issuecomment-1226590872
      inputs.nixpkgs.jdk11_headless
      inputs.nixpkgs.jq
      inputs.nixpkgs.python311
    ];
    source = [
      libGit
      outputs."/common/utils/sops"
      outputs."/integrates/streams/runtime"
    ];
  };
}
