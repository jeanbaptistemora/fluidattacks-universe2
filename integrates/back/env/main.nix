{
  inputs,
  libGit,
  makeTemplate,
  projectPath,
  outputs,
  ...
}:
makeTemplate {
  replace = {
    __argIntegrates__ = projectPath "/integrates";
    __argSecretsDev__ = projectPath "/integrates/secrets-development.yaml";
    __argSecretsProd__ = projectPath "/integrates/secrets-production.yaml";
    __argManifestFindings__ = projectPath "/skims/manifests/findings.json";
    __argManifestQueues__ = projectPath "/skims/manifests/queues.json";
  };
  name = "integrates-back-env";
  searchPaths = {
    rpath = [
      # Libmagic
      inputs.nixpkgs.file
      # Required by matplotlib
      inputs.nixpkgs.gcc.cc.lib
    ];
    bin = [
      # The binary to compute lines of code
      inputs.nixpkgs.cloc
      # The binary for pypi://GitPython
      inputs.nixpkgs.git
      # The binary for ssh
      inputs.nixpkgs.openssh
      # The binary to zip the data report
      inputs.nixpkgs.p7zip
    ];
    source = [
      libGit
      outputs."/integrates/back/tools"
      outputs."/integrates/back/pypi/runtime"
      outputs."/integrates/secrets/list"
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  template = ./template.sh;
}
