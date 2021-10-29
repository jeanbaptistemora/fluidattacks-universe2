{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  name = "makes-done";
  searchPaths = {
    bin = [
      inputs.nixpkgs.netcat
      outputs."/makes/kill-port"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
