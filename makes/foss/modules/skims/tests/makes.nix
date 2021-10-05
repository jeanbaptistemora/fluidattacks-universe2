{ __nixpkgs__
, inputs
, libGit
, makeTemplate
, outputs
, ...
}:
{
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
          "product" = __nixpkgs__.fetchFromGitLab {
            owner = "fluidattacks";
            repo = "product";
            rev = "ff231a9bf8aa3f0807f3431b402e7af08d136341";
            sha256 = "0rf65m2sqx9aswqsqrfhsiylw8g22cgzp80k8ir3bwa7pkb1s0ix";
            deepClone = true;
            leaveDotGit = true;
          };
          "VulnerableApp" = inputs.skimsVulnerableApp;
          "vulnerable_js_app" = inputs.skimsVulnerableJsApp;
        };
        searchPaths = {
          bin = [
            inputs.product.makes-wait
            inputs.product.makes-kill-port
            inputs.product.makes-kill-tree
            outputs."/skims/test/mocks/http"
            outputs."/skims/test/mocks/ssl/safe"
            outputs."/skims/test/mocks/ssl/unsafe"
          ];
          source = [
            inputs.product.skims-config-runtime
            outputs."/secretsForAwsFromEnv/skimsDev"
            outputs."/skims/env/development"
            (makeTemplate {
              name = "extra";
              searchPaths.source = [ libGit ];
              template = ./template.sh;
            })
          ];
        };
        extraFlags = [ "--reruns" "10" "--skims-test-group" category ];
      };
    })
    inputs.skimsTestPythonCategories);
}
