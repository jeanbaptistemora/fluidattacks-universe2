path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
  buildNodeRequirements = import (path "/makes/utils/build-node-requirements") path pkgs;
  nodeRequirements = buildNodeRequirements {
    name = "source-map-uploader";
    node = pkgs.nodejs;
    requirements = {
      direct = [
        "@bugsnag/source-maps@2.3.0"
      ];
      inherited = [
        "@babel/code-frame@7.14.5"
        "@babel/helper-validator-identifier@7.14.9"
        "@babel/highlight@7.14.5"
        "@types/normalize-package-data@2.4.1"
        "ansi-styles@3.2.1"
        "array-back@3.1.0"
        "asynckit@0.4.0"
        "balanced-match@1.0.2"
        "brace-expansion@1.1.11"
        "buffer-from@1.1.2"
        "chalk@2.4.2"
        "color-convert@1.9.3"
        "color-name@1.1.3"
        "combined-stream@1.0.8"
        "command-line-args@5.2.0"
        "command-line-usage@6.1.1"
        "concat-map@0.0.1"
        "concat-stream@2.0.0"
        "consola@2.15.3"
        "deep-extend@0.6.0"
        "delayed-stream@1.0.0"
        "error-ex@1.3.2"
        "escape-string-regexp@1.0.5"
        "find-replace@3.0.0"
        "find-up@4.1.0"
        "form-data@3.0.1"
        "fs.realpath@1.0.0"
        "function-bind@1.1.1"
        "glob@7.1.7"
        "has-flag@3.0.0"
        "has@1.0.3"
        "hosted-git-info@2.8.9"
        "inflight@1.0.6"
        "inherits@2.0.4"
        "is-arrayish@0.2.1"
        "is-core-module@2.6.0"
        "js-tokens@4.0.0"
        "json-parse-even-better-errors@2.3.1"
        "lines-and-columns@1.1.6"
        "locate-path@5.0.0"
        "lodash.camelcase@4.3.0"
        "mime-db@1.49.0"
        "mime-types@2.1.32"
        "minimatch@3.0.4"
        "normalize-package-data@2.5.0"
        "once@1.4.0"
        "p-limit@2.3.0"
        "p-locate@4.1.0"
        "p-try@2.2.0"
        "parse-json@5.2.0"
        "path-exists@4.0.0"
        "path-is-absolute@1.0.1"
        "path-parse@1.0.7"
        "read-pkg-up@7.0.1"
        "read-pkg@5.2.0"
        "readable-stream@3.6.0"
        "reduce-flatten@2.0.0"
        "resolve@1.20.0"
        "safe-buffer@5.2.1"
        "semver@5.7.1"
        "spdx-correct@3.1.1"
        "spdx-exceptions@2.3.0"
        "spdx-expression-parse@3.0.1"
        "spdx-license-ids@3.0.10"
        "string_decoder@1.3.0"
        "supports-color@5.5.0"
        "table-layout@1.0.2"
        "type-fest@0.8.1"
        "typedarray@0.0.6"
        "typical@4.0.0"
        "util-deprecate@1.0.2"
        "validate-npm-package-license@3.0.4"
        "wordwrapjs@4.0.1"
        "wrappy@1.0.2"
      ];
    };
  };
in
makeTemplate {
  name = "source-map-uploader";
  searchPaths = {
    envNodeBinaries = [ nodeRequirements ];
    envNodeLibraries = [ nodeRequirements ];
  };
  template = path "/makes/utils/source-map-uploader/template.sh";
}
