# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  outputs,
  projectPath,
  toBashMap,
  ...
}: {
  outputs = builtins.listToAttrs (builtins.map
    (category: {
      name = "/testPython/skims@${category}";
      value = makeScript {
        name = "skims-test-${category}";
        replace = {
          __argCategory__ = toString category;
          __argExtraSrcs__ = toBashMap {
            "androguard" = inputs.skimsAndroguard;
            "owasp_benchmark" = inputs.skimsBenchmarkOwasp;
            "NIST-SARD-Test-Suites" = inputs.skimsNistTestSuites;
            "universe" = builtins.path {
              name = "universe";
              path = ../..;
            };
            "VulnerableApp" = inputs.skimsVulnerableApp;
            "vulnerable_js_app" = inputs.skimsVulnerableJsApp;
          };
          __argProject__ = projectPath "/";
        };
        entrypoint = ./entrypoint.sh;
        searchPaths = {
          bin = [
            inputs.nixpkgs.gnugrep
            outputs."/common/utils/wait"
            outputs."/common/utils/kill/port"
            outputs."/common/utils/kill/tree"
            outputs."/skims/test/mocks/http"
            outputs."/skims/test/mocks/ssl/safe"
            outputs."/skims/test/mocks/ssl/unsafe"
          ];
          source = [
            outputs."/common/utils/aws"
            outputs."/skims/config/runtime"
            outputs."/skims/env/development"
          ];
        };
      };
    })
    inputs.skimsTestPythonCategories);
}
