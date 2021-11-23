{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "skims-test-cli";
  replace = {
    __argSecretsFile__ = projectPath "/skims/secrets/dev.yaml";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.gnugrep
      outputs."/skims"
      inputs.nixpkgs.kubectl
    ];
    source = [
      outputs."/secretsForAwsFromEnv/dev"
      outputs."/utils/sops"
      outputs."/utils/aws"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
