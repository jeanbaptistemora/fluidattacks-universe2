{ inputs
, makeScript
, makeNodeJsVersion
, outputs
, ...
}:
makeScript {
  name = "docs";
  replace = {
    __argNodeModules__ = outputs."/docs/runtime";
    __argSecretsAwsDev__ = outputs."/secretsForAwsFromEnv/docsDev";
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromEnv/docsProd";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.bash
      outputs."/docs/generate/criteria/vulns"
      (makeNodeJsVersion "12")
    ];
  };
  entrypoint = ./entrypoint.sh;
}
