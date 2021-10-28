{ inputs
, makeScript
, projectPath
, ...
}:
makeScript {
  replace = {
    __argAirsSecrets__ = projectPath "/airs/secrets";
    __argAirsNpm__ = inputs.product.airs-npm;
  };
  entrypoint = ./entrypoint.sh;
  name = "airs-config-development";
  searchPaths = {
    rpath = [
      inputs.nixpkgs.musl
    ];
    bin = [
      inputs.nixpkgs.utillinux
    ];
    source = [
      inputs.product.airs-npm-env
      inputs.product.airs-npm-runtime
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
}
