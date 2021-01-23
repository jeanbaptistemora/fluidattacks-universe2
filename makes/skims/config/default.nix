{ outputs
, path
, skimsPkgs
, skimsTreeSitterRepo
, ...
} @ _:
let
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path skimsPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path skimsPkgs;
in
{
  setupSkimsDevelopment = makeTemplate {
    arguments = {
      envSearchPaths = makeSearchPaths [ ];
      envPythonRequirements = outputs.packages.skims-config-python-requirements-development;
      envUtilsBashLibPython = path "/makes/utils/python.sh";
    };
    name = "skims-config-setup-skims-development";
    template = path "/makes/skims/config/setup-skims-development.sh";
  };

  setupSkimsRuntime = makeTemplate {
    arguments = {
      envContextFile = makeTemplate {
        arguments = {
          envParserAntlr = outputs.packages.skims-parsers-antlr;
          envParserBabel = outputs.packages.skims-parsers-babel;
          envSrcSkimsStatic = path "/skims/static";
          envSrcSkimsVendor = path "/skims/vendor";
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
      envSearchPaths = makeSearchPaths [
        skimsPkgs.graphviz
        skimsPkgs.nodejs
        skimsPkgs.python38Packages.pygraphviz
      ];
      envSrcSkimsSkims = path "/skims/skims";
      envUtilsBashLibPython = path "/makes/utils/python.sh";
    };
    name = "skims-config-setup-skims-runtime";
    template = path "/makes/skims/config/setup-skims-runtime.sh";
  };
}
