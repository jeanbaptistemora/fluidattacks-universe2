{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  name = "docs";
  replace = {
    __argSecretsAwsDev__ = outputs."/secretsForAwsFromEnv/dev";
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromEnv/prodDocs";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      outputs."/docs"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
