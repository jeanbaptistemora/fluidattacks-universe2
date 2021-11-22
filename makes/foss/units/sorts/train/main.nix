{ makeScript
, inputs
, outputs
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
  entrypoint = ./entrypoint.sh;
}
