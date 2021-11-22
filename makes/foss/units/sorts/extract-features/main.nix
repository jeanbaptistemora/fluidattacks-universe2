{ makeScript
, outputs
, ...
}:
makeScript {
  name = "sorts-extract-features";
  searchPaths = {
    source = [
      (outputs."/melts/lib")
      (outputs."/sorts/config-runtime")
      (outputs."/utils/aws")
      (outputs."/utils/git")
      (outputs."/utils/sops")
      (outputs."/utils/common")
    ];
  };
  entrypoint = ./entrypoint.sh;
}
