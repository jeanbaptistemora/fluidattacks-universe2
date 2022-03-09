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
      inputs.nixpkgs.nodejs
    ];
    source = [
      outputs."/airs/npm/runtime"
      outputs."/airs/npm/env"
      outputs."/utils/aws"
      outputs."/utils/lint-typescript"
      outputs."/utils/sops"
    ];
  };
}
