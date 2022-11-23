{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.job_last_success.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "observes-service-job-last-success-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
