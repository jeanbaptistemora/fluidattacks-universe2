{ buildNodeRequirements
, lintPython
, makes
, nixpkgs
, makeDerivation
, packages
, path
, ...
}:
let
  nodeRequirements = buildNodeRequirements {
    name = "integrates-charts-node-lint";
    node = nixpkgs.nodejs;
    requirements = {
      direct = [
        "eslint-config-strict@14.0.1"
        "eslint@7.3.1"
      ];
      inherited = [
        "@babel/code-frame@7.12.13"
        "@babel/helper-validator-identifier@7.12.11"
        "@babel/highlight@7.12.13"
        "acorn-jsx@5.3.1"
        "acorn@7.4.1"
        "ajv-keywords@2.1.1"
        "ajv@6.12.6"
        "ansi-colors@4.1.1"
        "ansi-escapes@3.2.0"
        "ansi-regex@5.0.0"
        "ansi-styles@3.2.1"
        "argparse@1.0.10"
        "astral-regex@1.0.0"
        "babel-code-frame@6.26.0"
        "balanced-match@1.0.0"
        "brace-expansion@1.1.11"
        "buffer-from@1.1.1"
        "caller-path@0.1.0"
        "callsites@3.1.0"
        "chalk@4.1.0"
        "chardet@0.4.2"
        "circular-json@0.3.3"
        "cli-cursor@2.1.0"
        "cli-width@2.2.1"
        "co@4.6.0"
        "color-convert@1.9.3"
        "color-name@1.1.3"
        "concat-map@0.0.1"
        "concat-stream@1.6.2"
        "core-util-is@1.0.2"
        "cross-spawn@7.0.3"
        "debug@4.3.1"
        "deep-is@0.1.3"
        "doctrine@3.0.0"
        "emoji-regex@7.0.3"
        "enquirer@2.3.6"
        "escape-string-regexp@1.0.5"
        "eslint-plugin-filenames@1.3.2"
        "eslint-scope@5.1.1"
        "eslint-utils@2.1.0"
        "eslint-visitor-keys@1.3.0"
        "espree@7.3.1"
        "esprima@4.0.1"
        "esquery@1.4.0"
        "esrecurse@4.3.0"
        "estraverse@4.3.0"
        "esutils@2.0.3"
        "external-editor@2.2.0"
        "fast-deep-equal@3.1.3"
        "fast-json-stable-stringify@2.1.0"
        "fast-levenshtein@2.0.6"
        "figures@2.0.0"
        "file-entry-cache@5.0.1"
        "flat-cache@2.0.1"
        "flatted@2.0.2"
        "fs.realpath@1.0.0"
        "functional-red-black-tree@1.0.1"
        "glob-parent@5.1.1"
        "glob@7.1.6"
        "globals@12.4.0"
        "graceful-fs@4.2.6"
        "has-ansi@2.0.0"
        "has-flag@3.0.0"
        "iconv-lite@0.4.24"
        "ignore@4.0.6"
        "import-fresh@3.3.0"
        "imurmurhash@0.1.4"
        "inflight@1.0.6"
        "inherits@2.0.4"
        "inquirer@3.3.0"
        "is-extglob@2.1.1"
        "is-fullwidth-code-point@2.0.0"
        "is-glob@4.0.1"
        "is-resolvable@1.1.0"
        "isarray@1.0.0"
        "isexe@2.0.0"
        "js-tokens@4.0.0"
        "js-yaml@3.14.1"
        "json-schema-traverse@0.4.1"
        "json-stable-stringify-without-jsonify@1.0.1"
        "levn@0.4.1"
        "lodash.camelcase@4.3.0"
        "lodash.kebabcase@4.1.1"
        "lodash.snakecase@4.1.1"
        "lodash.upperfirst@4.3.1"
        "lodash@4.17.21"
        "lru-cache@6.0.0"
        "mimic-fn@1.2.0"
        "minimatch@3.0.4"
        "minimist@1.2.5"
        "mkdirp@0.5.5"
        "ms@2.1.2"
        "mute-stream@0.0.7"
        "natural-compare@1.4.0"
        "object-assign@4.1.1"
        "once@1.4.0"
        "onetime@2.0.1"
        "optionator@0.9.1"
        "os-tmpdir@1.0.2"
        "parent-module@1.0.1"
        "path-is-absolute@1.0.1"
        "path-is-inside@1.0.2"
        "path-key@3.1.1"
        "pluralize@7.0.0"
        "prelude-ls@1.2.1"
        "process-nextick-args@2.0.1"
        "progress@2.0.3"
        "pseudomap@1.0.2"
        "punycode@2.1.1"
        "readable-stream@2.3.7"
        "regexpp@3.1.0"
        "require-uncached@1.0.3"
        "resolve-from@4.0.0"
        "restore-cursor@2.0.0"
        "rimraf@2.6.3"
        "run-async@2.4.1"
        "rx-lite-aggregates@4.0.8"
        "rx-lite@4.0.8"
        "safe-buffer@5.1.2"
        "safer-buffer@2.1.2"
        "semver@7.3.4"
        "shebang-command@2.0.0"
        "shebang-regex@3.0.0"
        "signal-exit@3.0.3"
        "slice-ansi@2.1.0"
        "sprintf-js@1.0.3"
        "string-width@3.1.0"
        "string_decoder@1.1.1"
        "strip-ansi@6.0.0"
        "strip-json-comments@3.1.1"
        "supports-color@5.5.0"
        "table@5.4.6"
        "text-table@0.2.0"
        "through@2.3.8"
        "tmp@0.0.33"
        "type-check@0.4.0"
        "type-fest@0.8.1"
        "typedarray@0.0.6"
        "uri-js@4.4.1"
        "util-deprecate@1.0.2"
        "v8-compile-cache@2.2.0"
        "which@2.0.2"
        "word-wrap@1.2.3"
        "wrappy@1.0.2"
        "write@1.0.3"
        "yallist@4.0.0"
      ];
    };
  };
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "charts-lint-python-lint";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeDerivation {
  arguments = {
    envChartsSrc = path "/integrates/charts";
    envGraphsSrc = path "/integrates/back/src/app/templates/static/graphics";
  };
  builder = path "/makes/packages/integrates/charts/lint/builder.sh";
  name = "integrates-charts-lint";
  searchPaths = {
    envNodeBinaries = [ nodeRequirements ];
    envNodeLibraries = [ nodeRequirements ];
    envSources = [
      lintPython
      packages.integrates.back.pypi.runtime
      pythonRequirements
    ];
  };
}
