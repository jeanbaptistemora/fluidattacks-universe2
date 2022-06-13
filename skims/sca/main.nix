{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "skims-sca-update";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python38
      outputs."/skims"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
      outputs."/skims/config/runtime"
    ];
  };

  replace = {
    __argUpdateSCA__ = "sca/update/__init__.py";
  };

  entrypoint = ./entrypoint.sh;
}
