{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argManifests__ = ./k8s;
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.gnugrep
      inputs.nixpkgs.utillinux
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/integrates/back/deploy/lib"
    ];
  };
  name = "integrates-back-deploy-dev";
  entrypoint = ./entrypoint.sh;
}
