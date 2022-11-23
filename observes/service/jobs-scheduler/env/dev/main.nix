{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.scheduler.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-service-jobs-scheduler-env-runtime";
    searchPaths = {
      bin = [env];
      export = import ../bins.nix {inherit outputs;};
    };
  }
