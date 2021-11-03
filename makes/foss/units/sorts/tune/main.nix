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
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/sorts/tune/entrypoint.sh";
}
