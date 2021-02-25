{ buildNodeRequirements
, makeEntrypoint
, makesPkgs
, path
, ...
}:
let
  nodeRequirements = buildNodeRequirements makesPkgs {
    name = "makes-announce-bugsnag";
    node = makesPkgs.nodejs;
    requirements = {
      direct = [
        "bugsnag-build-reporter@1.0.3"
      ];
      inherited = [
        "ansi-styles@3.2.1"
        "array-find-index@1.0.2"
        "arrify@1.0.1"
        "buffer-from@1.1.1"
        "camelcase-keys@4.2.0"
        "camelcase@4.1.0"
        "chalk@2.4.2"
        "color-convert@1.9.3"
        "color-name@1.1.3"
        "concat-stream@1.6.2"
        "core-util-is@1.0.2"
        "currently-unhandled@0.4.1"
        "decamelize-keys@1.1.0"
        "decamelize@1.2.0"
        "end-of-stream@1.4.4"
        "error-ex@1.3.2"
        "escape-string-regexp@1.0.5"
        "fast-json-parse@1.0.3"
        "fast-safe-stringify@1.2.3"
        "find-nearest-file@1.1.0"
        "find-up@2.1.0"
        "flatstr@1.0.12"
        "function-bind@1.1.1"
        "graceful-fs@4.2.6"
        "has-flag@3.0.0"
        "has@1.0.3"
        "hosted-git-info@2.8.8"
        "indent-string@3.2.0"
        "inherits@2.0.4"
        "is-arrayish@0.2.1"
        "is-core-module@2.2.0"
        "is-plain-obj@1.1.0"
        "isarray@1.0.0"
        "json-parse-better-errors@1.0.2"
        "load-json-file@4.0.0"
        "locate-path@2.0.0"
        "loud-rejection@1.6.0"
        "map-obj@2.0.0"
        "meow@4.0.1"
        "minimist-options@3.0.2"
        "minimist@1.2.5"
        "normalize-package-data@2.5.0"
        "once@1.4.0"
        "p-limit@1.3.0"
        "p-locate@2.0.0"
        "p-try@1.0.0"
        "parse-json@4.0.0"
        "path-exists@3.0.0"
        "path-parse@1.0.6"
        "path-type@3.0.0"
        "pify@3.0.0"
        "pino-std-serializers@2.5.0"
        "pino@4.17.6"
        "process-nextick-args@2.0.1"
        "pump@3.0.0"
        "queue-microtask@1.2.2"
        "quick-format-unescaped@1.1.2"
        "quick-lru@1.1.0"
        "read-pkg-up@3.0.0"
        "read-pkg@3.0.0"
        "readable-stream@2.3.7"
        "redent@2.0.0"
        "resolve@1.20.0"
        "run-parallel@1.2.0"
        "safe-buffer@5.1.2"
        "semver@5.7.1"
        "signal-exit@3.0.3"
        "spdx-correct@3.1.1"
        "spdx-exceptions@2.3.0"
        "spdx-expression-parse@3.0.1"
        "spdx-license-ids@3.0.7"
        "split2@2.2.0"
        "string_decoder@1.1.1"
        "strip-bom@3.0.0"
        "strip-indent@2.0.0"
        "supports-color@5.5.0"
        "through2@2.0.5"
        "trim-newlines@2.0.0"
        "typedarray@0.0.6"
        "util-deprecate@1.0.2"
        "validate-npm-package-license@3.0.4"
        "wrappy@1.0.2"
        "xtend@4.0.2"
      ];
    };
  };
in
makeEntrypoint makesPkgs {
  name = "makes-announce-bugsnag";
  searchPaths = {
    envNodeBinaries = [ nodeRequirements ];
    envNodeLibraries = [ nodeRequirements ];
  };
  template = path "/makes/applications/makes/announce/bugsnag/entrypoint.sh";
}
