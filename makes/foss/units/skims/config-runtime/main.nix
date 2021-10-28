{ inputs
, makeTemplate
, projectPath
, outputs
, ...
}:
makeTemplate {
  replace = {
    __argSrcSkimsSkims__ = projectPath "/skims/skims";
  };
  name = "skims-config-runtime";
  searchPaths = {
    bin = [
      inputs.nixpkgs.gcc
      inputs.nixpkgs.git
      inputs.nixpkgs.graphviz
      inputs.nixpkgs.nodejs
    ];
    pythonPackage = [
      (projectPath "/skims/skims")
    ];
    source = [
      outputs."/makes/python/safe-pickle"
      outputs."/skims/config-runtime/pypi"
      (makeTemplate {
        replace = {
          __argCriteriaRequirements__ =
            projectPath "/makes/foss/modules/makes/criteria/src/requirements/data.yaml";
          __argCriteriaVulnerabilities__ =
            projectPath "/makes/foss/modules/makes/criteria/src/vulnerabilities/data.yaml";
          __argSkimsProcessGroupOnAws__ =
            outputs."/computeOnAwsBatch/skimsProcessGroup";
          __argSrcTreeSitterParsers__ = outputs."/skims/config-runtime/parsers";
          __argSrcSkimsStatic__ = projectPath "/skims/static";
          __argSrcSkimsVendor__ = projectPath "/skims/vendor";
        };
        name = "skims-config-context-file";
        template = ''
          # There is no problem in making this key public
          #   it's intentional so we can monitor Skims stability in remote users
          export BUGSNAG_API_KEY=f990c9a571de4cb44c96050ff0d50ddb
          export SKIMS_CIPHER_SUITES_PATH='__argSrcSkimsStatic__/cryptography/cipher_suites.csv'
          export SKIMS_CRITERIA_REQUIREMENTS='__argCriteriaRequirements__'
          export SKIMS_CRITERIA_VULNERABILITIES='__argCriteriaVulnerabilities__'
          export SKIMS_FLUID_WATERMARK='__argSrcSkimsStatic__/img/logo_fluid_attacks_854x329.png'
          export SKIMS_PROCESS_GROUP_ON_AWS='__argSkimsProcessGroupOnAws__/bin/compute-on-aws-batch-for-skimsProcessGroup'
          export SKIMS_ROBOTO_FONT='__argSrcSkimsVendor__/fonts/roboto_mono_from_google/regular.ttf'
          export SKIMS_STATIC='__argSrcSkimsStatic__'
          export SKIMS_TREE_SITTER_PARSERS='__argSrcTreeSitterParsers__'
          export SKIMS_VENDOR='__argSrcSkimsVendor__'
        '';
      })
    ];
  };
  template = projectPath "/makes/foss/units/skims/config-runtime/template.sh";
}
