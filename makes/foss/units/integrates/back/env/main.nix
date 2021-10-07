{ inputs
, libGit
, makeTemplate
, projectPath
, outputs
, ...
}:
makeTemplate {
  replace = {
    __argIntegrates__ = projectPath "/integrates";
    __argSecretsDev__ = projectPath "/integrates/secrets-development.yaml";
    __argSecretsProd__ = projectPath "/integrates/secrets-production.yaml";
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
      # The binary for pypi://GitPython
      inputs.nixpkgs.git
      # The binary for the ASGI
      inputs.nixpkgs.python39Packages.gunicorn
      # The binary to zip the data report
      inputs.nixpkgs.p7zip
    ];
    source = [
      outputs."/integrates/back/tools"
      outputs."/integrates/back/pypi/runtime"
      outputs."/integrates/secrets/list"
      outputs."/skims/config-sdk"
      libGit
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  template = projectPath "/makes/foss/units/integrates/back/env/template.sh";
}
