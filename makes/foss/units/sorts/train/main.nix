{ makeScript
, inputs
, outputs
, projectPath
, ...
}:
makeScript {
  name = "sorts-train";
  searchPaths = {
    bin = [ inputs.nixpkgs.python38 ];
    source = [
      outputs."/sorts/config-development"
      outputs."/sorts/config-runtime"
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/sorts/train/entrypoint.sh";
}
