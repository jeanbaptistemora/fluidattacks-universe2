{ makeScript
, outputs
, ...
}:
makeScript {
  name = "sorts-execute";
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
