{
  inputs,
  libGit,
  makeScript,
  makeTemplate,
  outputs,
  projectPath,
  toBashMap,
  ...
}: let
  categories = [
    "functional"
    "cli"
  ];
in {
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
            outputs."/common/utils/wait"
            outputs."/common/utils/kill/port"
            outputs."/common/utils/kill/tree"
            outputs."/skims/test/mocks/http"
            outputs."/skims/test/mocks/ssl/safe"
            outputs."/skims/test/mocks/ssl/unsafe"
          ];
          source = [
            outputs."/skims/config/runtime"
            outputs."/skims/env/development"
            (makeTemplate {
              name = "extra";
              searchPaths = {
                source = [
                  libGit
                  outputs."/common/utils/sops"
                  outputs."/common/utils/aws"
                ];
                bin = [
                  inputs.nixpkgs.kubectl
                ];
              };
              replace = {
                __argSecretsFile__ = projectPath "/skims/secrets/dev.yaml";
                __argIsFunctionalTest__ = builtins.elem category categories;
              };
              template = ./template.sh;
            })
          ];
        };
      };
    })
    inputs.skimsTestPythonCategories);
}
