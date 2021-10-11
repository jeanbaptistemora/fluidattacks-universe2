{ makeScript
, inputs
, outputs
, projectPath
, ...
}:
makeScript {
  name = "sorts-tune";
  searchPaths = {
    bin = [ inputs.nixpkgs.python38 ];
    source = [
      outputs."/sorts/config-development"
      outputs."/sorts/config-runtime"
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/sorts/tune/entrypoint.sh";
}
