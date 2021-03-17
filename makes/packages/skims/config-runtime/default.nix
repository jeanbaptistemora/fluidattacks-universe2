{ buildPythonRequirements
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
      nixpkgs.python38Packages.pygraphviz
      (buildPythonRequirements {
        name = "skims-runtime";
        requirements = {
          direct = [
            "aioextensions==20.9.2315218"
            "aiofiles==0.5.0"
            "aiogqlc==2.0.0b1"
            "aiohttp==3.6.2"
            "bugsnag==3.8.0"
            "cfn-flip==1.2.3"
            "click==7.1.2"
            "confuse==1.3.0"
            "frozendict==1.2"
            "GitPython==3.1.13"
            "jmespath==0.10.0"
            "lark-parser==0.7.8"
            "metaloaders==20.9.2566091"
            "more-itertools==8.4.0"
            "networkx==2.5"
            "oyaml==0.9"
            "Pillow==7.2.0"
            "pyparsing==2.4.7"
            "python-dateutil==2.8.1"
            "python-hcl2==0.3.0"
            "python-jose==3.2.0"
            "requests==2.24.0"
            "ruamel.yaml.clib==0.2.2"
            "ruamel.yaml==0.16.10"
            "semver==2.10.2"
            "tracers==20.7.17562"
            "tree-sitter==0.19.0"
            "uvloop==0.14.0"
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
            "gitdb==4.0.5"
            "idna==2.10"
            "multidict==4.7.6"
            "pyasn1==0.4.8"
            "PyYAML==5.4.1"
            "rsa==4.7.2"
            "s3transfer==0.3.4"
            "six==1.15.0"
            "smmap==3.0.5"
            "typing-extensions==3.7.4.3"
            "urllib3==1.25.11"
            "WebOb==1.8.7"
            "wrapt==1.12.1"
            "yarl==1.6.3"
          ];
        };
        python = nixpkgs.python38;
      })
    ];
    envSources = [
      (makeTemplate {
        arguments = {
          envParserAntlr = packages.skims.parsers.antlr;
          envParserBabel = packages.skims.parsers.babel;
          envSrcSkimsStatic = path "/skims/static";
          envSrcSkimsVendor = path "/skims/vendor";
          envSrcTreeSitter = fetchzip {
            url = "https://github.com/fluidattacks/tree-sitter-java/archive/318b7bca0f703541e6f1061e20962015da28f444.tar.gz";
            sha256 = "7lLHvA9lv5CTO/gJ+KBmRIVFQ5bTYQPlMhqrrIcRdno=";
          };
        };
        name = "skims-config-context-file";
        template = ''
          export SKIMS_CIPHER_SUITES_PATH='__envSrcSkimsStatic__/cryptography/cipher_suites.csv'
          export SKIMS_FLUID_WATERMARK='__envSrcSkimsStatic__/img/logo_fluid_attacks_854x329.png'
          export SKIMS_PARSER_ANTLR='__envParserAntlr__/build/install/parse/bin/parse'
          export SKIMS_PARSER_BABEL='__envParserBabel__'
          export SKIMS_ROBOTO_FONT='__envSrcSkimsVendor__/fonts/roboto_mono_from_google/regular.ttf'
          export SKIMS_STATIC='__envSrcSkimsStatic__'
          export SKIMS_TREE_SITTER_JAVA='__envSrcTreeSitter__'
          export SKIMS_VENDOR='__envSrcSkimsVendor__'
        '';
      })
    ];
  };
  template = path "/makes/packages/skims/config-runtime/template.sh";
}
