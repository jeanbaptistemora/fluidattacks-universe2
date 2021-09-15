{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  name = "docs";
  replace = {
    __argSecretsAwsDev__ = outputs."/secretsForAwsFromEnv/docsDev";
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromEnv/docsProd";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      outputs."/docs"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
