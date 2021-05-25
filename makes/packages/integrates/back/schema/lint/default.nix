{ buildNodeRequirements
, makeDerivation
, nixpkgs
, path
, ...
} @ _:
let
  nodeRequirements = buildNodeRequirements {
    name = "integrates-back-schema-lint-npm";
    node = nixpkgs.nodejs;
    requirements = {
      direct = [
        "graphql-schema-linter@2.0.1"
      ];
      inherited = [
        "ansi-regex@2.1.1"
        "ansi-styles@3.2.1"
        "argparse@1.0.10"
        "balanced-match@1.0.2"
        "brace-expansion@1.1.11"
        "caller-callsite@2.0.0"
        "caller-path@2.0.0"
        "callsites@2.0.0"
        "chalk@2.4.2"
        "clone@1.0.4"
        "color-convert@1.9.3"
        "color-name@1.1.3"
        "columnify@1.5.4"
        "commander@3.0.2"
        "concat-map@0.0.1"
        "cosmiconfig@5.2.1"
        "defaults@1.0.3"
        "error-ex@1.3.2"
        "escape-string-regexp@1.0.5"
        "esprima@4.0.1"
        "fs.realpath@1.0.0"
        "glob@7.1.7"
        "graphql@15.5.0"
        "has-flag@3.0.0"
        "import-fresh@2.0.0"
        "inflight@1.0.6"
        "inherits@2.0.4"
        "is-arrayish@0.2.1"
        "is-directory@0.3.1"
        "js-yaml@3.14.1"
        "json-parse-better-errors@1.0.2"
        "minimatch@3.0.4"
        "once@1.4.0"
        "parse-json@4.0.0"
        "path-is-absolute@1.0.1"
        "resolve-from@3.0.0"
        "sprintf-js@1.0.3"
        "strip-ansi@3.0.1"
        "supports-color@5.5.0"
        "wcwidth@1.0.1"
        "wrappy@1.0.2"
      ];
    };
  };
in
makeDerivation {
  arguments = {
    envNodeRequirements = nodeRequirements;
    envIntegratesApiSchema = path "/integrates/back/src/api/schema";
  };
  builder = path "/makes/packages/integrates/back/schema/lint/builder.sh";
  name = "integrates-back-schema-lint";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
    ];
  };
}
