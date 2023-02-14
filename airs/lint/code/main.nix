{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argAirsFront__ = projectPath "/airs/front";
    __argAirsNpm__ = outputs."/airs/npm";
    __argAirsSecrets__ = projectPath "/airs/secrets";
  };
  entrypoint = ./entrypoint.sh;
  name = "airs-lint-code";
  searchPaths = {
    bin = [
      inputs.nixpkgs.nodejs-18_x
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/airs/npm/runtime"
      outputs."/airs/npm/env"
      outputs."/common/utils/lint-npm-deps"
      outputs."/common/utils/lint-typescript"
      outputs."/common/utils/sops"
    ];
  };
}
