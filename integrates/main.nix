{
  fetchGithub,
  inputs,
  makeScript,
  toFileYaml,
  ...
}: let
  config = toFileYaml "mprocs.yaml" {
    procs = {
      back.cmd = ["m" "." "/integrates/back" "dev"];
      db.cmd = ["m" "." "/integrates/db"];
      front.cmd = ["m" "." "/integrates/front"];
      storage.cmd = ["m" "." "/integrates/storage/dev"];
    };
  };
  makes = import (fetchGithub {
    owner = "fluidattacks";
    repo = "makes";
    rev = "bd2848c799aac0f04e211f16547dad41c6e3190e";
    sha256 = "4L0pGjx20rymK0mZgeLKZ9AiALhWya4nhC32/9gYSqM=";
  }) {};
in
  makeScript {
    entrypoint = "mprocs --config __argConfig__";
    name = "integrates";
    replace.__argConfig__ = config;
    searchPaths.bin = [
      inputs.nixpkgs.mprocs
      makes
    ];
  }
