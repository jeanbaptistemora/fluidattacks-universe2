{ fetchGithub
, inputs
, makePythonPypiEnvironment
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
      inputs.nixpkgs.python38
    ];
    pythonPackage = [
      (projectPath "/skims/skims")
    ];
    pythonPackage38 = [
      inputs.nixpkgs.python38Packages.asn1crypto
      inputs.nixpkgs.python38Packages.androguard
      inputs.nixpkgs.python38Packages.beautifulsoup4
      inputs.nixpkgs.python38Packages.future
      inputs.nixpkgs.python38Packages.lxml
      inputs.nixpkgs.python38Packages.ntplib
      inputs.nixpkgs.python38Packages.pygments
      inputs.nixpkgs.python38Packages.pygraphviz
      inputs.nixpkgs.python38Packages.soupsieve
      inputs.nixpkgs.python38Packages.unidiff
      inputs.nixpkgs.python38Packages.viewstate
    ];
    source = [
      inputs.product.makes-python-safe-pickle
      outputs."/skims/config-sdk"
      (makePythonPypiEnvironment {
        name = "skims-runtime";
        searchPaths = {
          bin = [ inputs.nixpkgs.gcc ];
        };
        sourcesYaml = ./pypi-sources.yaml;
        withSetuptools_57_4_0 = true;
        withWheel_0_37_0 = true;
      })
      (makeTemplate {
        replace = {
          __argCriteriaRequirements__ =
            projectPath "/makes/foss/modules/makes/criteria/src/requirements/data.yaml";
          __argCriteriaVulnerabilities__ =
            projectPath "/makes/foss/modules/makes/criteria/src/vulnerabilities/data.yaml";
          __argSkimsProcessGroupOnAws__ =
            outputs."/computeOnAwsBatch/skimsProcessGroup";
          __argSrcSkimsStatic__ = projectPath "/skims/static";
          __argSrcSkimsVendor__ = projectPath "/skims/vendor";
          __argSrcTreeSitterCSharp__ = fetchGithub {
            owner = "tree-sitter";
            repo = "tree-sitter-c-sharp";
            rev = "851ac4735f66ec9c479096cc21bf58519da49faa";
            sha256 = "UHw5JQ++iYLTyqL8KH1impRxXJ2oJAQRoD79nLVQgMw=";
          };
          __argSrcTreeSitterGo__ = fetchGithub {
            owner = "tree-sitter";
            repo = "tree-sitter-go";
            rev = "eb306e6e60f393df346cfc8cbfaf52667a37128a";
            sha256 = "7LD8wR4Gg4OadYaXTSbGPe5iAOagRPGJSpO51uW0ow8=";
          };
          __argSrcTreeSitterJava__ = fetchGithub {
            owner = "tree-sitter";
            repo = "tree-sitter-java";
            rev = "2efe37f92d2e6aeb25186e9da07455bb4a30163c";
            sha256 = "09v3xg1356ghc2n0yi8iqkp80lbkav0jpfgz8iz2j1sl7ihbvkyw";
          };
          __argSrcTreeSitterJavaScript__ = fetchGithub {
            owner = "tree-sitter";
            repo = "tree-sitter-javascript";
            rev = "45b9ce2a2588c0e6d616b0ee2a710b1fcb99c5b5";
            sha256 = "nU0mVkGG6Sr4OstRFCIrbUGJnAHMZ9+lCDTJAFf392c=";
          };
          __argSrcTreeSitterKotlin__ = fetchGithub {
            owner = "tree-sitter";
            repo = "tree-sitter-kotlin";
            rev = "48bfb38abd93f8d617877d7bb7f92a6bb1166285";
            sha256 = "5thm7nYOZLDUsb/2KGV2fZg35uId8nZEMdyLUsdTPT0=";
          };
          __argSrcTreeSitterTsx__ = fetchGithub {
            owner = "tree-sitter";
            repo = "tree-sitter-typescript";
            rev = "3e897ea5925f037cfae2e551f8e6b12eec2a201a";
            sha256 = "1qJsaeJzcbSTDe9hqc9SjPhGG0RNaolTYQLuwgryIsw=";
          };
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
          export SKIMS_TREE_SITTER_CSHARP='__argSrcTreeSitterCSharp__'
          export SKIMS_TREE_SITTER_GO='__argSrcTreeSitterGo__'
          export SKIMS_TREE_SITTER_JAVA='__argSrcTreeSitterJava__'
          export SKIMS_TREE_SITTER_JAVASCRIPT='__argSrcTreeSitterJavaScript__'
          export SKIMS_TREE_SITTER_KOTLIN='__argSrcTreeSitterKotlin__'
          export SKIMS_TREE_SITTER_TSX='__argSrcTreeSitterTsx__/tsx'
          export SKIMS_VENDOR='__argSrcSkimsVendor__'
        '';
      })
    ];
  };
  template = projectPath "/makes/foss/units/skims/config-runtime/template.sh";
}
