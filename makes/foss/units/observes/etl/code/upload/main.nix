{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/code/bin"
      outputs."/melts"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/git"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-code-upload";
  entrypoint = ./entrypoint.sh;
}
