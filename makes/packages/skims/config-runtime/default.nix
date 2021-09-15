{ applications
, fetchzip
, makes
, makeTemplate
, packages
, path
, nixpkgs
, ...
}:
makeTemplate {
  arguments = {
    envSrcSkimsSkims = path "/skims/skims";
  };
  name = "skims-config-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.gcc
      nixpkgs.git
      nixpkgs.graphviz
      nixpkgs.nodejs
      nixpkgs.python38
    ];
    envPythonPaths = [
      (path "/skims/skims")
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.asn1crypto
      nixpkgs.python38Packages.androguard
      nixpkgs.python38Packages.beautifulsoup4
      nixpkgs.python38Packages.future
      nixpkgs.python38Packages.lxml
      nixpkgs.python38Packages.ntplib
      nixpkgs.python38Packages.pygments
      nixpkgs.python38Packages.pygraphviz
      nixpkgs.python38Packages.soupsieve
      nixpkgs.python38Packages.unidiff
      nixpkgs.python38Packages.viewstate
    ];
    envSources = [
      packages.makes.python.safe-pickle
      packages.skims.config-sdk
      (makes.makePythonPypiEnvironment {
        name = "skims-runtime";
        searchPaths = {
          bin = [ nixpkgs.gcc ];
        };
        sourcesYaml = ./pypi-sources.yaml;
        withSetuptools_57_4_0 = true;
        withWheel_0_37_0 = true;
      })
      (makeTemplate {
        arguments = {
          envCriteriaRequirements = path "/makes/foss/modules/makes/criteria/src/requirements/data.yaml";
          envCriteriaVulnerabilities = path "/makes/foss/modules/makes/criteria/src/vulnerabilities/data.yaml";
          envSkimsProcessGroupOnAws = applications.skims.process-group-on-aws;
          envSrcSkimsStatic = path "/skims/static";
          envSrcSkimsVendor = path "/skims/vendor";
          envSrcTreeSitterCSharp = fetchzip {
            url = "https://github.com/tree-sitter/tree-sitter-c-sharp/archive/851ac4735f66ec9c479096cc21bf58519da49faa.tar.gz";
            sha256 = "UHw5JQ++iYLTyqL8KH1impRxXJ2oJAQRoD79nLVQgMw=";
          };
          envSrcTreeSitterGo = fetchzip {
            url = "https://github.com/tree-sitter/tree-sitter-go/archive/eb306e6e60f393df346cfc8cbfaf52667a37128a.tar.gz";
            sha256 = "7LD8wR4Gg4OadYaXTSbGPe5iAOagRPGJSpO51uW0ow8=";
          };
          envSrcTreeSitterJava = fetchzip {
            url = "https://github.com/tree-sitter/tree-sitter-java/archive/2efe37f92d2e6aeb25186e9da07455bb4a30163c.tar.gz";
            sha256 = "09v3xg1356ghc2n0yi8iqkp80lbkav0jpfgz8iz2j1sl7ihbvkyw";
          };
          envSrcTreeSitterJavaScript = fetchzip {
            url = "https://github.com/tree-sitter/tree-sitter-javascript/archive/45b9ce2a2588c0e6d616b0ee2a710b1fcb99c5b5.tar.gz";
            sha256 = "nU0mVkGG6Sr4OstRFCIrbUGJnAHMZ9+lCDTJAFf392c=";
          };
          envSrcTreeSitterKotlin = fetchzip {
            url = "https://github.com/tormodatt/tree-sitter-kotlin/archive/48bfb38abd93f8d617877d7bb7f92a6bb1166285.zip";
            sha256 = "5thm7nYOZLDUsb/2KGV2fZg35uId8nZEMdyLUsdTPT0=";
          };
          envSrcTreeSitterTsx = fetchzip {
            url = "https://github.com/tree-sitter/tree-sitter-typescript/archive/3e897ea5925f037cfae2e551f8e6b12eec2a201a.tar.gz";
            sha256 = "1qJsaeJzcbSTDe9hqc9SjPhGG0RNaolTYQLuwgryIsw=";
          };
        };
        name = "skims-config-context-file";
        template = ''
          # There is no problem in making this key public
          #   it's intentional so we can monitor Skims stability in remote users
          export BUGSNAG_API_KEY=f990c9a571de4cb44c96050ff0d50ddb
          export SKIMS_CIPHER_SUITES_PATH='__envSrcSkimsStatic__/cryptography/cipher_suites.csv'
          export SKIMS_CRITERIA_REQUIREMENTS='__envCriteriaRequirements__'
          export SKIMS_CRITERIA_VULNERABILITIES='__envCriteriaVulnerabilities__'
          export SKIMS_FLUID_WATERMARK='__envSrcSkimsStatic__/img/logo_fluid_attacks_854x329.png'
          export SKIMS_PROCESS_GROUP_ON_AWS='__envSkimsProcessGroupOnAws__'
          export SKIMS_ROBOTO_FONT='__envSrcSkimsVendor__/fonts/roboto_mono_from_google/regular.ttf'
          export SKIMS_STATIC='__envSrcSkimsStatic__'
          export SKIMS_TREE_SITTER_CSHARP='__envSrcTreeSitterCSharp__'
          export SKIMS_TREE_SITTER_GO='__envSrcTreeSitterGo__'
          export SKIMS_TREE_SITTER_JAVA='__envSrcTreeSitterJava__'
          export SKIMS_TREE_SITTER_JAVASCRIPT='__envSrcTreeSitterJavaScript__'
          export SKIMS_TREE_SITTER_KOTLIN='__envSrcTreeSitterKotlin__'
          export SKIMS_TREE_SITTER_TSX='__envSrcTreeSitterTsx__/tsx'
          export SKIMS_VENDOR='__envSrcSkimsVendor__'
        '';
      })
    ];
  };
  template = path "/makes/packages/skims/config-runtime/template.sh";
}
