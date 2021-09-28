{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  name = "skims-test-cli";
  searchPaths.bin = [
    inputs.nixpkgs.gnugrep
    outputs."/skims"
  ];
  entrypoint = ./entrypoint.sh;
}
