# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
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
    __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
    __argSecretsProd__ = projectPath "/integrates/secrets/production.yaml";
    __argManifestFindings__ = projectPath "/skims/manifests/findings.json";
    __argManifestQueues__ = projectPath "/skims/manifests/queues.json";
    __argCriteriaRequirements__ = projectPath "/common/criteria/src/requirements/data.yaml";
    __argCriteriaVulnerabilities__ = projectPath "/common/criteria/src/vulnerabilities/data.yaml";
    __argSrcSkimsVendor__ = projectPath "/skims/vendor";
    __argSrcSkimsStatic__ = projectPath "/skims/static";
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
      # The binary for ssh
      inputs.nixpkgs.openssh
      # The binary to zip the data report
      inputs.nixpkgs.p7zip
    ];
    source = [
      libGit
      outputs."/integrates/back/tools"
      outputs."/integrates/back/env/pypi/runtime"
      outputs."/integrates/secrets/list"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  template = ./template.sh;
}
