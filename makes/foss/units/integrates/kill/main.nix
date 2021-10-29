{ makeScript
, outputs
, ...
}:
makeScript {
  name = "integrates-kill";
  searchPaths.bin = [
    outputs."/makes/kill-port"
  ];
  entrypoint = ./entrypoint.sh;
}
