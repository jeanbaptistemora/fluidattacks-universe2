{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argManifests__ = projectPath "/integrates/back/deploy/dev/k8s";
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
