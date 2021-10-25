{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  name = "melts-test";
  searchPaths = {
    source = [
      outputs."/melts/config-development"
      inputs.product.melts-config-runtime
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
    ];
    bin = [
      inputs.nixpkgs.gnugrep
    ];
  };
  entrypoint = ./entrypoint.sh;
}
