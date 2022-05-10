{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "common-users-infra-rotate-keys";
  searchPaths = {
    bin = [
      outputs."/integrates/back/deploy/prod"
      outputs."/taintTerraform/commonUsersKeys1"
      outputs."/taintTerraform/commonUsersKeys2"
    ];
    source = [
      outputs."/common/utils/aws"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
