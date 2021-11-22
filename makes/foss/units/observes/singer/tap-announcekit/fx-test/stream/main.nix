{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/singer/tap-announcekit/bin"
    ];
    source = [
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-singer-tap-announcekit-fx-test-stream";
  entrypoint = ./entrypoint.sh;
}
