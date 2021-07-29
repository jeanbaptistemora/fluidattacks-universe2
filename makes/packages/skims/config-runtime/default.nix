{ applications
, buildPythonRequirements
, fetchzip
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
      (buildPythonRequirements {
        name = "skims-runtime";
        requirements = {
          direct = [
            "aioextensions==20.11.1621472"
            "aiofiles==0.6.0"
            "aiogqlc==2.0.0b1"
            "aiohttp==3.7.4"
            "bugsnag==4.0.3"
            "cfn-flip==1.2.3"
            "click==7.1.2"
            "confuse==1.4.0"
            "frozendict==2.0.2"
            "GitPython==3.1.15"
            "jmespath==0.10.0"
            "lark-parser==0.7.8" # pending to upgrade
            "metaloaders==20.9.2566091"
            "more-itertools==8.7.0"
            "mypy-extensions==0.4.3"
            "networkx==2.5.1"
            "oyaml==1.0"
            "Pillow==8.2.0"
            "pyparsing==2.4.7"
            "python-dateutil==2.8.1"
            "python-hcl2==1.0.0" # pending to upgrade
            "python-jose==3.2.0"
            "requests==2.25.1"
            "ruamel.yaml.clib==0.2.2"
            "ruamel.yaml==0.17.4"
            "semver==2.13.0"
            "tlslite-ng==0.8.0a41"
            "tracers==20.7.17562"
            "tree-sitter==0.19.0"
            "uvloop==0.15.2"
          ];
          inherited = [
            "aioboto3==8.0.3"
            "aiobotocore==1.0.4"
            "aioitertools==0.7.1"
            "async-timeout==3.0.1"
            "attrs==20.3.0"
            "boto3==1.12.32"
            "botocore==1.15.32"
            "certifi==2020.12.5"
            "chardet==3.0.4"
            "decorator==4.4.2"
            "docutils==0.15.2"
            "ecdsa==0.14.1"
            "gitdb==4.0.7"
            "idna==2.10"
            "multidict==5.1.0"
            "pyasn1==0.4.8"
            "PyYAML==5.4.1"
            "rsa==4.7.2"
            "s3transfer==0.3.7"
            "six==1.15.0"
            "smmap==4.0.0"
            "typing-extensions==3.10.0.0"
            "urllib3==1.26.4"
            "WebOb==1.8.7"
            "wrapt==1.12.1"
            "yarl==1.6.3"
          ];
        };
        python = nixpkgs.python38;
      })
    ];
    envSources = [
      packages.makes.python.safe-pickle
      (makeTemplate {
        arguments = {
          envCriteriaRequirements = path "/makes/makes/criteria/src/requirements/data.yaml";
          envCriteriaVulnerabilities = path "/makes/makes/criteria/src/vulnerabilities/data.yaml";
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
            url = "https://github.com/tree-sitter/tree-sitter-java/archive/8d6a858350475386b6fd58210c34750a8f361b6a.tar.gz";
            sha256 = "fhN+yKPfGkpA/QIUSkzczXF0EOGPbwoCYlyEjDUtgg0=";
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
