{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "docs-deploy";
  replace = {
    __argSecretsAwsDev__ = outputs."/secretsForAwsFromGitlab/dev";
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromGitlab/prodDocs";
  };

  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      outputs."/docs"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
