{ inputs
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
          "product" = inputs.nixpkgs.fetchgit {
            url = "https://gitlab.com/fluidattacks/product.git";
            rev = "ff231a9bf8aa3f0807f3431b402e7af08d136341";
            sha256 = "03ik2di2bjvn2q02rf6mvfiiy3f27dyny9k48nwipkdb9bhcdxpf";
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
            inputs.product.skims-test-mocks-ssl-safe
            inputs.product.skims-test-mocks-ssl-unsafe
            outputs."/skims/test/mocks/http"
          ];
          source = [
            inputs.product.skims-config-development
            inputs.product.skims-config-runtime
            outputs."/secretsForAwsFromEnv/skimsDev"
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
