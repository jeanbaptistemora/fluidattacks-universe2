{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/gitlab"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-gitlab-challenges";
  entrypoint = ./entrypoint.sh;
}
