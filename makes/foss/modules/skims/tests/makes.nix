{
  inputs,
  libGit,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  categories = [
    "functional"
    "cli"
  ];
in {
  testPython = builtins.listToAttrs (builtins.map
    (category: {
      name = "skims@${category}";
      value = {
        python = "3.8";
        src = "/skims";
        extraSrcs = {
          "androguard" = inputs.skimsAndroguard;
          "owasp_benchmark" = inputs.skimsBenchmarkOwasp;
          "NIST-SARD-Test-Suites" = inputs.skimsNistTestSuites;
          "product" = builtins.path {
            name = "product";
            path = ../../../../..;
          };
          "VulnerableApp" = inputs.skimsVulnerableApp;
          "vulnerable_js_app" = inputs.skimsVulnerableJsApp;
        };
        searchPaths = {
          bin = [
            outputs."/makes/wait"
            outputs."/makes/kill-port"
            outputs."/makes/kill-tree"
            outputs."/skims/test/mocks/http"
            outputs."/skims/test/mocks/ssl/safe"
            outputs."/skims/test/mocks/ssl/unsafe"
          ];
          source = [
            outputs."/secretsForAwsFromEnv/dev"
            outputs."/skims/config-runtime"
            outputs."/skims/env/development"
            (makeTemplate {
              name = "extra";
              searchPaths = {
                source = [
                  libGit
                  outputs."/utils/sops"
                  outputs."/utils/aws"
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
        extraFlags = ["--reruns" "1" "--skims-test-group" category];
      };
    })
    inputs.skimsTestPythonCategories);
}
