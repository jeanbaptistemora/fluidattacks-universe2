_ @ {
  outputs,
  skimsPkgs,
  skimsTreeSitterRepo,
  ...
}:

let
  makeSearchPaths = import ../../../makes/utils/make-search-paths skimsPkgs;
  makeTemplate = import ../../../makes/utils/make-template skimsPkgs;
  nixRequirements = {
    development = makeSearchPaths [];
    runtime = makeSearchPaths [
      skimsPkgs.graphviz
      skimsPkgs.python38Packages.pygraphviz
    ];
  };
in
  {
    setupSkimsDevelopment = makeTemplate {
      arguments = {
        envBinPath = nixRequirements.development.binPath;
        envLibPath = nixRequirements.development.libPath;
        envPyPath = nixRequirements.development.pyPath;
        envPythonRequirements = outputs.packages.skims-config-python-requirements-development;
        envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
      };
      name = "skims-config-setup-skims-development";
      template = ../../../makes/skims/config/setup-skims-development.sh;
    };

    setupSkimsRuntime = makeTemplate {
      arguments = {
        envContextFile = makeTemplate {
          arguments = {
            envParserAntlr = outputs.packages.skims-parsers-antlr;
            envParserBabel = outputs.packages.skims-parsers-babel;
            envSrcSkimsStatic = ../../../skims/static;
            envSrcSkimsVendor = ../../../skims/vendor;
            envSrcTreeSitter = skimsTreeSitterRepo;
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
        };
        envPython = "${skimsPkgs.python38}/bin/python";
        envPythonRequirements = outputs.packages.skims-config-python-requirements-runtime;
        envBinPath = nixRequirements.runtime.binPath;
        envLibPath = nixRequirements.runtime.libPath;
        envPyPath = nixRequirements.runtime.pyPath;
        envSrcSkimsSkims = ../../../skims/skims;
        envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
      };
      name = "skims-config-setup-skims-runtime";
      template = ../../../makes/skims/config/setup-skims-runtime.sh;
    };
  }
