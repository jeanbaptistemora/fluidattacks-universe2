{
  makeScript,
  outputs,
  inputs,
  ...
}:
makeScript {
  name = "common-users-infra-rotate-keys";
  searchPaths = {
    bin = [
      inputs.nixpkgs.which
      outputs."/integrates/back/deploy/prod"
      outputs."/taintTerraform/commonUsersKeys1"
      outputs."/taintTerraform/commonUsersKeys2"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
