{
  inputs,
  makeScript,
  ...
}:
makeScript {
  replace = {
    __argSrc__ = ./src;
  };
  name = "common-foss-gitlab-clean-artifacts";
  searchPaths.bin = [inputs.nixpkgs.go];
  entrypoint = ./entrypoint.sh;
}
