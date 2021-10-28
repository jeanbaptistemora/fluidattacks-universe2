{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  replace = {
    __argAirsNpm__ = outputs."/airs/npm";
    __argAirsSecrets__ = projectPath "/airs/secrets";
  };
  entrypoint = ./entrypoint.sh;
  name = "airs-build";
  searchPaths = {
    rpath = [
      inputs.nixpkgs.musl
    ];
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnugrep
      inputs.nixpkgs.gnused
      inputs.nixpkgs.nodejs
      inputs.nixpkgs.utillinux
    ];
    source = [
      outputs."/airs/npm/runtime"
      outputs."/airs/npm/env"
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
}
