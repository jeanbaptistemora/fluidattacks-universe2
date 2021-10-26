{ inputs
, makeScript
, projectPath
, ...
}:
makeScript {
  replace = {
    __argAirsFront__ = projectPath "/airs/front";
    __argAirsNpm__ = inputs.product.airs-npm;
    __argAirsSecrets__ = projectPath "/airs/secrets";
  };
  entrypoint = ./entrypoint.sh;
  name = "airs-lint-code";
  searchPaths = {
    bin = [
      inputs.nixpkgs.nodejs
    ];
    source = [
      inputs.product.airs-npm-runtime
      inputs.product.airs-npm-env
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "lint-typescript")
      (inputs.legacy.importUtility "sops")
    ];
  };
}
