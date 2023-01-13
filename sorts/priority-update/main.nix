{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "priority-update";
  searchPaths = {
    source = [
      outputs."/sorts/config/runtime"
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
      outputs."/common/utils/sops"
      outputs."/common/utils/common"
      outputs."/observes/common/list-groups"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
