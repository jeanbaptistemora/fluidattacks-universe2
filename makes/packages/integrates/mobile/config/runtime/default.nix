{ path
, integratesPkgs
, ...
} @ _:
let
  buildNodeRequirements = import (path "/makes/utils/build-node-requirements") path integratesPkgs;
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
  getPackageJsonDeps = import (path "/makes/utils/get-package-json-deps") path integratesPkgs;
  nodeRequirements = buildNodeRequirements {
    dependencies = [ ];
    name = "integrates-mobile-runtime";
    node = integratesPkgs.nodejs-12_x;
    requirements = {
      direct = (getPackageJsonDeps {
        packageJsonPath = "/integrates/mobile/package.json";
      }).production;
      inherited = [
        "@babel/code-frame@7.12.13"
        "@babel/compat-data@7.12.13"
        "@babel/core@7.9.0"
        "@babel/generator@7.12.13"
        "@babel/helper-annotate-as-pure@7.12.13"
        "@babel/helper-builder-binary-assignment-operator-visitor@7.12.13"
        "@babel/helper-compilation-targets@7.12.13"
        "@babel/helper-create-class-features-plugin@7.12.13"
        "@babel/helper-create-regexp-features-plugin@7.12.13"
        "@babel/helper-explode-assignable-expression@7.12.13"
        "@babel/helper-function-name@7.12.13"
        "@babel/helper-get-function-arity@7.12.13"
        "@babel/helper-hoist-variables@7.12.13"
        "@babel/helper-member-expression-to-functions@7.12.13"
        "@babel/helper-module-imports@7.12.13"
        "@babel/helper-module-transforms@7.12.13"
        "@babel/helper-optimise-call-expression@7.12.13"
        "@babel/helper-plugin-utils@7.12.13"
        "@babel/helper-remap-async-to-generator@7.12.13"
        "@babel/helper-replace-supers@7.12.13"
        "@babel/helper-simple-access@7.12.13"
        "@babel/helper-skip-transparent-expression-wrappers@7.12.1"
        "@babel/helper-split-export-declaration@7.12.13"
        "@babel/helper-validator-identifier@7.12.11"
        "@babel/helper-validator-option@7.12.11"
        "@babel/helper-wrap-function@7.12.13"
        "@babel/helpers@7.12.13"
        "@babel/highlight@7.12.13"
        "@babel/parser@7.12.14"
        "@babel/plugin-external-helpers@7.12.13"
        "@babel/plugin-proposal-async-generator-functions@7.12.13"
        "@babel/plugin-proposal-class-properties@7.12.13"
        "@babel/plugin-proposal-decorators@7.12.13"
        "@babel/plugin-proposal-dynamic-import@7.12.1"
        "@babel/plugin-proposal-export-default-from@7.12.13"
        "@babel/plugin-proposal-export-namespace-from@7.12.13"
        "@babel/plugin-proposal-json-strings@7.12.13"
        "@babel/plugin-proposal-logical-assignment-operators@7.12.13"
        "@babel/plugin-proposal-nullish-coalescing-operator@7.12.13"
        "@babel/plugin-proposal-numeric-separator@7.12.13"
        "@babel/plugin-proposal-object-rest-spread@7.12.13"
        "@babel/plugin-proposal-optional-catch-binding@7.12.13"
        "@babel/plugin-proposal-optional-chaining@7.12.13"
        "@babel/plugin-proposal-private-methods@7.12.13"
        "@babel/plugin-proposal-unicode-property-regex@7.12.13"
        "@babel/plugin-syntax-async-generators@7.8.4"
        "@babel/plugin-syntax-class-properties@7.12.13"
        "@babel/plugin-syntax-decorators@7.12.13"
        "@babel/plugin-syntax-dynamic-import@7.8.3"
        "@babel/plugin-syntax-export-default-from@7.12.13"
        "@babel/plugin-syntax-export-namespace-from@7.8.3"
        "@babel/plugin-syntax-flow@7.12.13"
        "@babel/plugin-syntax-json-strings@7.8.3"
        "@babel/plugin-syntax-jsx@7.12.13"
        "@babel/plugin-syntax-logical-assignment-operators@7.10.4"
        "@babel/plugin-syntax-nullish-coalescing-operator@7.8.3"
        "@babel/plugin-syntax-numeric-separator@7.10.4"
        "@babel/plugin-syntax-object-rest-spread@7.8.3"
        "@babel/plugin-syntax-optional-catch-binding@7.8.3"
        "@babel/plugin-syntax-optional-chaining@7.8.3"
        "@babel/plugin-syntax-top-level-await@7.12.13"
        "@babel/plugin-syntax-typescript@7.12.13"
        "@babel/plugin-transform-arrow-functions@7.12.13"
        "@babel/plugin-transform-async-to-generator@7.12.13"
        "@babel/plugin-transform-block-scoped-functions@7.12.13"
        "@babel/plugin-transform-block-scoping@7.12.13"
        "@babel/plugin-transform-classes@7.12.13"
        "@babel/plugin-transform-computed-properties@7.12.13"
        "@babel/plugin-transform-destructuring@7.12.13"
        "@babel/plugin-transform-dotall-regex@7.12.13"
        "@babel/plugin-transform-duplicate-keys@7.12.13"
        "@babel/plugin-transform-exponentiation-operator@7.12.13"
        "@babel/plugin-transform-flow-strip-types@7.12.13"
        "@babel/plugin-transform-for-of@7.12.13"
        "@babel/plugin-transform-function-name@7.12.13"
        "@babel/plugin-transform-literals@7.12.13"
        "@babel/plugin-transform-member-expression-literals@7.12.13"
        "@babel/plugin-transform-modules-amd@7.12.13"
        "@babel/plugin-transform-modules-commonjs@7.12.13"
        "@babel/plugin-transform-modules-systemjs@7.12.13"
        "@babel/plugin-transform-modules-umd@7.12.13"
        "@babel/plugin-transform-named-capturing-groups-regex@7.12.13"
        "@babel/plugin-transform-new-target@7.12.13"
        "@babel/plugin-transform-object-assign@7.12.13"
        "@babel/plugin-transform-object-super@7.12.13"
        "@babel/plugin-transform-parameters@7.12.13"
        "@babel/plugin-transform-property-literals@7.12.13"
        "@babel/plugin-transform-react-display-name@7.12.13"
        "@babel/plugin-transform-react-jsx-self@7.12.13"
        "@babel/plugin-transform-react-jsx-source@7.12.13"
        "@babel/plugin-transform-react-jsx@7.12.13"
        "@babel/plugin-transform-regenerator@7.12.13"
        "@babel/plugin-transform-reserved-words@7.12.13"
        "@babel/plugin-transform-runtime@7.12.13"
        "@babel/plugin-transform-shorthand-properties@7.12.13"
        "@babel/plugin-transform-spread@7.12.13"
        "@babel/plugin-transform-sticky-regex@7.12.13"
        "@babel/plugin-transform-template-literals@7.12.13"
        "@babel/plugin-transform-typeof-symbol@7.12.13"
        "@babel/plugin-transform-typescript@7.12.13"
        "@babel/plugin-transform-unicode-escapes@7.12.13"
        "@babel/plugin-transform-unicode-regex@7.12.13"
        "@babel/preset-env@7.12.13"
        "@babel/preset-modules@0.1.4"
        "@babel/preset-typescript@7.12.13"
        "@babel/register@7.12.13"
        "@babel/runtime@7.12.13"
        "@babel/template@7.12.13"
        "@babel/traverse@7.12.13"
        "@babel/types@7.12.13"
        "@bugsnag/cuid@3.0.0"
        "@bugsnag/delivery-expo@7.6.0"
        "@bugsnag/plugin-browser-session@7.6.0"
        "@bugsnag/plugin-console-breadcrumbs@7.6.0"
        "@bugsnag/plugin-expo-app@7.6.0"
        "@bugsnag/plugin-expo-device@7.6.0"
        "@bugsnag/plugin-network-breadcrumbs@7.6.0"
        "@bugsnag/plugin-react-native-app-state-breadcrumbs@7.6.0"
        "@bugsnag/plugin-react-native-connectivity-breadcrumbs@7.6.0"
        "@bugsnag/plugin-react-native-global-error-handler@7.6.0"
        "@bugsnag/plugin-react-native-orientation-breadcrumbs@7.6.0"
        "@bugsnag/plugin-react-native-unhandled-rejection@7.6.0"
        "@bugsnag/safe-json-stringify@6.0.0"
        "@bugsnag/source-maps@1.0.1"
        "@callstack/react-theme-provider@3.0.5"
        "@cnakazawa/watch@1.0.4"
        "@expo/babel-preset-cli@0.2.18"
        "@expo/config-plugins@1.0.18"
        "@expo/config-types@40.0.0-beta.2"
        "@expo/config@3.3.28"
        "@expo/configure-splash-screen@0.3.3"
        "@expo/image-utils@0.3.10"
        "@expo/json-file@8.2.27"
        "@expo/metro-config@0.1.54"
        "@expo/plist@0.0.11"
        "@expo/spawn-async@1.5.0"
        "@expo/websql@1.0.1"
        "@graphql-typed-document-node/core@3.1.0"
        "@hapi/address@2.1.4"
        "@hapi/bourne@1.3.2"
        "@hapi/hoek@8.5.1"
        "@hapi/joi@15.1.1"
        "@hapi/topo@3.1.6"
        "@ide/backoff@1.0.0"
        "@jest/console@24.9.0"
        "@jest/fake-timers@24.9.0"
        "@jest/source-map@24.9.0"
        "@jest/test-result@24.9.0"
        "@jest/types@26.6.2"
        "@jimp/bmp@0.12.1"
        "@jimp/core@0.12.1"
        "@jimp/custom@0.12.1"
        "@jimp/gif@0.12.1"
        "@jimp/jpeg@0.12.1"
        "@jimp/plugin-blit@0.12.1"
        "@jimp/plugin-blur@0.12.1"
        "@jimp/plugin-circle@0.12.1"
        "@jimp/plugin-color@0.12.1"
        "@jimp/plugin-contain@0.12.1"
        "@jimp/plugin-cover@0.12.1"
        "@jimp/plugin-crop@0.12.1"
        "@jimp/plugin-displace@0.12.1"
        "@jimp/plugin-dither@0.12.1"
        "@jimp/plugin-fisheye@0.12.1"
        "@jimp/plugin-flip@0.12.1"
        "@jimp/plugin-gaussian@0.12.1"
        "@jimp/plugin-invert@0.12.1"
        "@jimp/plugin-mask@0.12.1"
        "@jimp/plugin-normalize@0.12.1"
        "@jimp/plugin-print@0.12.1"
        "@jimp/plugin-resize@0.12.1"
        "@jimp/plugin-rotate@0.12.1"
        "@jimp/plugin-scale@0.12.1"
        "@jimp/plugin-shadow@0.12.1"
        "@jimp/plugin-threshold@0.12.1"
        "@jimp/plugins@0.12.1"
        "@jimp/png@0.12.1"
        "@jimp/tiff@0.12.1"
        "@jimp/types@0.12.1"
        "@jimp/utils@0.12.1"
        "@react-native-community/cli-debugger-ui@4.13.1"
        "@react-native-community/cli-hermes@4.13.0"
        "@react-native-community/cli-platform-android@4.13.0"
        "@react-native-community/cli-platform-ios@4.13.0"
        "@react-native-community/cli-server-api@4.13.1"
        "@react-native-community/cli-tools@4.13.0"
        "@react-native-community/cli-types@4.10.1"
        "@react-native-community/netinfo@5.9.7"
        "@types/istanbul-lib-coverage@2.0.3"
        "@types/istanbul-lib-report@3.0.0"
        "@types/istanbul-reports@3.0.0"
        "@types/node@14.14.24"
        "@types/normalize-package-data@2.4.0"
        "@types/stack-utils@1.0.1"
        "@types/ungap__global-this@0.3.1"
        "@types/yargs-parser@20.2.0"
        "@types/yargs@15.0.13"
        "@types/zen-observable@0.8.2"
        "@ungap/global-this@0.4.4"
        "@unimodules/core@6.0.0"
        "@unimodules/react-native-adapter@5.7.0"
        "@wry/context@0.5.3"
        "@wry/equality@0.3.1"
        "@wry/trie@0.2.1"
        "abort-controller@3.0.0"
        "absolute-path@0.0.0"
        "accepts@1.3.7"
        "anser@1.4.10"
        "ansi-colors@1.1.0"
        "ansi-cyan@0.1.1"
        "ansi-escapes@3.2.0"
        "ansi-fragments@0.2.1"
        "ansi-gray@0.1.1"
        "ansi-red@0.1.1"
        "ansi-regex@5.0.0"
        "ansi-styles@3.2.1"
        "ansi-wrap@0.1.0"
        "any-base@1.1.0"
        "anymatch@2.0.0"
        "argparse@1.0.10"
        "argsarray@0.0.1"
        "arr-diff@4.0.0"
        "arr-flatten@1.1.0"
        "arr-union@3.1.0"
        "array-back@3.1.0"
        "array-filter@0.0.1"
        "array-find-index@1.0.2"
        "array-map@0.0.0"
        "array-reduce@0.0.0"
        "array-slice@0.2.3"
        "array-unique@0.3.2"
        "arrify@1.0.1"
        "asap@2.0.6"
        "assert@2.0.0"
        "assign-symbols@1.0.0"
        "astral-regex@1.0.0"
        "async@2.6.3"
        "asynckit@0.4.0"
        "at-least-node@1.0.0"
        "atob@2.1.2"
        "available-typed-arrays@1.0.2"
        "babel-plugin-dynamic-import-node@2.3.3"
        "babel-plugin-module-resolver@3.2.0"
        "babel-plugin-react-native-web@0.13.18"
        "babel-plugin-syntax-trailing-function-commas@7.0.0-beta.0"
        "babel-preset-expo@8.3.0"
        "babel-preset-fbjs@3.3.0"
        "badgin@1.2.2"
        "balanced-match@1.0.0"
        "base64-js@1.5.1"
        "base@0.11.2"
        "big-integer@1.6.48"
        "bindings@1.5.0"
        "blueimp-md5@2.18.0"
        "bmp-js@0.1.0"
        "boolbase@1.0.0"
        "bplist-creator@0.0.8"
        "bplist-parser@0.2.0"
        "brace-expansion@1.1.11"
        "braces@2.3.2"
        "browserslist@4.16.3"
        "bser@2.1.1"
        "buffer-alloc-unsafe@1.1.0"
        "buffer-alloc@1.2.0"
        "buffer-crc32@0.2.13"
        "buffer-equal@0.0.1"
        "buffer-fill@1.0.0"
        "buffer-from@1.1.1"
        "buffer@5.7.1"
        "bugsnag-build-reporter@1.0.3"
        "bytes@3.0.0"
        "cache-base@1.0.1"
        "call-bind@1.0.2"
        "caller-callsite@2.0.0"
        "caller-path@2.0.0"
        "callsites@2.0.0"
        "camelcase-keys@4.2.0"
        "camelcase@4.1.0"
        "caniuse-lite@1.0.30001183"
        "capture-exit@2.0.0"
        "chalk@2.4.2"
        "chardet@0.4.2"
        "ci-info@2.0.0"
        "class-utils@0.3.6"
        "cli-cursor@2.1.0"
        "cli-spinners@2.5.0"
        "cli-width@2.2.1"
        "cliui@6.0.0"
        "clone@1.0.4"
        "collection-visit@1.0.0"
        "color-convert@1.9.3"
        "color-name@1.1.3"
        "color-string@1.5.4"
        "color-support@1.1.3"
        "color@3.1.3"
        "colorette@1.2.1"
        "combined-stream@1.0.8"
        "command-exists@1.2.9"
        "command-line-args@5.1.1"
        "command-line-usage@6.1.1"
        "commander@5.1.0"
        "commondir@1.0.1"
        "compare-urls@2.0.0"
        "compare-versions@3.6.0"
        "component-emitter@1.3.0"
        "compressible@2.0.18"
        "compression@1.7.4"
        "concat-map@0.0.1"
        "concat-stream@2.0.0"
        "connect@3.7.0"
        "consola@2.15.2"
        "convert-source-map@1.7.0"
        "copy-descriptor@0.1.1"
        "core-js-compat@3.8.3"
        "core-js@3.8.3"
        "core-util-is@1.0.2"
        "cosmiconfig@5.2.1"
        "cross-spawn@6.0.5"
        "crypto-random-string@1.0.0"
        "css-select@2.1.0"
        "css-tree@1.1.2"
        "css-what@3.4.2"
        "currently-unhandled@0.4.1"
        "dayjs@1.10.4"
        "debug@4.3.1"
        "decamelize-keys@1.1.0"
        "decamelize@1.2.0"
        "decode-uri-component@0.2.0"
        "deep-equal@2.0.5"
        "deep-extend@0.6.0"
        "deepmerge@3.3.0"
        "defaults@1.0.3"
        "define-properties@1.1.3"
        "define-property@2.0.2"
        "delayed-stream@1.0.0"
        "denodeify@1.2.1"
        "depd@1.1.2"
        "destroy@1.0.4"
        "dom-serializer@0.2.2"
        "dom-walk@0.1.2"
        "domelementtype@1.3.1"
        "domutils@1.7.0"
        "ee-first@1.1.1"
        "electron-to-chromium@1.3.653"
        "emoji-regex@8.0.0"
        "encodeurl@1.0.2"
        "encoding@0.1.13"
        "end-of-stream@1.4.4"
        "entities@2.2.0"
        "envinfo@7.7.4"
        "error-ex@1.3.2"
        "error-stack-parser@2.0.6"
        "errorhandler@1.5.1"
        "es-abstract@1.18.0-next.2"
        "es-get-iterator@1.1.2"
        "es-to-primitive@1.2.1"
        "es6-object-assign@1.1.0"
        "escalade@3.1.1"
        "escape-html@1.0.3"
        "escape-string-regexp@1.0.5"
        "esprima@4.0.1"
        "esutils@2.0.3"
        "etag@1.8.1"
        "event-target-shim@5.0.1"
        "eventemitter3@3.1.2"
        "exec-sh@0.3.4"
        "execa@1.0.0"
        "exif-parser@0.1.12"
        "expand-brackets@2.1.4"
        "expo-application@2.4.1"
        "expo-asset@8.2.2"
        "expo-crypto@8.4.0"
        "expo-error-recovery@1.4.0"
        "expo-file-system@9.3.0"
        "expo-font@8.4.0"
        "expo-keep-awake@8.4.0"
        "expo-linear-gradient@8.4.0"
        "expo-linking@2.0.1"
        "expo-location@10.0.0"
        "expo-sqlite@8.5.0"
        "extend-shallow@3.0.2"
        "external-editor@2.2.0"
        "extglob@2.0.4"
        "fancy-log@1.3.3"
        "fast-json-parse@1.0.3"
        "fast-json-stable-stringify@2.1.0"
        "fast-safe-stringify@1.2.3"
        "fb-watchman@2.0.1"
        "fbemitter@2.1.1"
        "fbjs-css-vars@1.0.2"
        "fbjs-scripts@1.2.0"
        "fbjs@1.0.0"
        "figures@2.0.0"
        "file-type@9.0.0"
        "file-uri-to-path@1.0.0"
        "fill-range@4.0.0"
        "finalhandler@1.1.2"
        "find-babel-config@1.2.0"
        "find-cache-dir@2.1.0"
        "find-nearest-file@1.1.0"
        "find-replace@3.0.0"
        "find-up@5.0.0"
        "flatstr@1.0.12"
        "fontfaceobserver@2.1.0"
        "for-in@1.0.2"
        "foreach@2.0.5"
        "form-data@3.0.0"
        "fragment-cache@0.2.1"
        "fresh@0.5.2"
        "fs-extra@9.0.0"
        "fs.realpath@1.0.0"
        "fsevents@1.2.13"
        "function-bind@1.1.1"
        "gensync@1.0.0-beta.2"
        "get-caller-file@2.0.5"
        "get-intrinsic@1.1.1"
        "get-stream@4.1.0"
        "get-value@2.0.6"
        "getenv@0.7.0"
        "glob@7.1.6"
        "global@4.4.0"
        "globals@11.12.0"
        "graceful-fs@4.2.4"
        "graphql-tag@2.11.0"
        "has-flag@3.0.0"
        "has-symbols@1.0.1"
        "has-value@1.0.0"
        "has-values@1.0.0"
        "has@1.0.3"
        "hermes-engine@0.5.1"
        "hermes-profile-transformer@0.0.6"
        "history@4.10.1"
        "hoist-non-react-statics@3.3.2"
        "hosted-git-info@2.8.8"
        "html-parse-stringify2@2.0.1"
        "http-errors@1.7.3"
        "iconv-lite@0.6.2"
        "ieee754@1.2.1"
        "image-size@0.6.3"
        "immediate@3.3.0"
        "import-fresh@2.0.0"
        "imurmurhash@0.1.4"
        "indent-string@3.2.0"
        "inflight@1.0.6"
        "inherits@2.0.4"
        "inquirer@3.3.0"
        "invariant@2.2.4"
        "ip@1.1.5"
        "is-accessor-descriptor@0.1.6"
        "is-arguments@1.1.0"
        "is-arrayish@0.3.2"
        "is-bigint@1.0.1"
        "is-boolean-object@1.1.0"
        "is-buffer@1.1.6"
        "is-callable@1.2.3"
        "is-ci@2.0.0"
        "is-core-module@2.2.0"
        "is-data-descriptor@0.1.4"
        "is-date-object@1.0.2"
        "is-descriptor@0.1.6"
        "is-directory@0.3.1"
        "is-extendable@0.1.1"
        "is-fullwidth-code-point@2.0.0"
        "is-function@1.0.2"
        "is-generator-function@1.0.8"
        "is-map@2.0.2"
        "is-nan@1.3.2"
        "is-negative-zero@2.0.1"
        "is-number-object@1.0.4"
        "is-number@3.0.0"
        "is-plain-obj@1.1.0"
        "is-plain-object@2.0.4"
        "is-regex@1.1.2"
        "is-set@2.0.2"
        "is-stream@1.1.0"
        "is-string@1.0.5"
        "is-symbol@1.0.3"
        "is-typed-array@1.1.4"
        "is-weakmap@2.0.1"
        "is-weakset@2.0.1"
        "is-windows@1.0.2"
        "is-wsl@1.1.0"
        "isarray@2.0.5"
        "iserror@0.0.2"
        "isexe@2.0.0"
        "isobject@3.0.1"
        "isomorphic-fetch@2.2.1"
        "iterall@1.3.0"
        "jest-get-type@24.9.0"
        "jest-haste-map@24.9.0"
        "jest-message-util@24.9.0"
        "jest-mock@24.9.0"
        "jest-serializer@24.9.0"
        "jest-util@24.9.0"
        "jest-validate@24.9.0"
        "jest-worker@24.9.0"
        "jetifier@1.6.6"
        "jimp@0.12.1"
        "jpeg-js@0.4.3"
        "js-tokens@4.0.0"
        "js-yaml@3.14.1"
        "jsc-android@245459.0.0"
        "jsesc@2.5.2"
        "json-parse-better-errors@1.0.2"
        "json-parse-even-better-errors@2.3.1"
        "json-stable-stringify@1.0.1"
        "json5@2.2.0"
        "jsonfile@6.1.0"
        "jsonify@0.0.0"
        "kind-of@6.0.3"
        "klaw@1.3.1"
        "leven@3.1.0"
        "lines-and-columns@1.1.6"
        "load-bmfont@1.4.1"
        "load-json-file@4.0.0"
        "locate-path@6.0.0"
        "lodash._reinterpolate@3.0.0"
        "lodash.camelcase@4.3.0"
        "lodash.frompairs@4.0.1"
        "lodash.isequal@4.5.0"
        "lodash.isstring@4.0.1"
        "lodash.omit@4.5.0"
        "lodash.pick@4.4.0"
        "lodash.template@4.5.0"
        "lodash.templatesettings@4.2.0"
        "lodash.throttle@4.1.1"
        "log-symbols@2.2.0"
        "logkitty@0.7.1"
        "loose-envify@1.4.0"
        "loud-rejection@1.6.0"
        "lru-cache@4.1.5"
        "make-dir@2.1.0"
        "makeerror@1.0.11"
        "map-cache@0.2.2"
        "map-obj@2.0.0"
        "map-visit@1.0.0"
        "md5-file@3.2.3"
        "mdn-data@2.0.14"
        "meow@4.0.1"
        "merge-stream@1.0.1"
        "metro-babel-register@0.59.0"
        "metro-babel-transformer@0.58.0"
        "metro-cache@0.58.0"
        "metro-config@0.58.0"
        "metro-core@0.58.0"
        "metro-inspector-proxy@0.58.0"
        "metro-minify-uglify@0.58.0"
        "metro-react-native-babel-preset@0.59.0"
        "metro-react-native-babel-transformer@0.58.0"
        "metro-resolver@0.58.0"
        "metro-source-map@0.58.0"
        "metro-symbolicate@0.58.0"
        "metro@0.58.0"
        "micromatch@3.1.10"
        "mime-db@1.45.0"
        "mime-types@2.1.28"
        "mime@2.5.0"
        "mimic-fn@1.2.0"
        "min-document@2.19.0"
        "mini-create-react-context@0.4.1"
        "minimatch@3.0.4"
        "minimist-options@3.0.2"
        "minimist@1.2.5"
        "mixin-deep@1.3.2"
        "mkdirp@0.5.5"
        "ms@2.1.2"
        "mute-stream@0.0.7"
        "nan@2.14.2"
        "nanomatch@1.2.13"
        "negotiator@0.6.2"
        "nice-try@1.0.5"
        "nocache@2.1.0"
        "node-fetch@2.6.1"
        "node-int64@0.4.0"
        "node-modules-regexp@1.0.0"
        "node-releases@1.1.70"
        "node-stream-zip@1.12.0"
        "noop-fn@1.0.0"
        "normalize-package-data@2.5.0"
        "normalize-path@2.1.1"
        "normalize-url@2.0.1"
        "npm-run-path@2.0.2"
        "nth-check@1.0.2"
        "nullthrows@1.1.1"
        "ob1@0.58.0"
        "object-assign@4.1.1"
        "object-copy@0.1.0"
        "object-inspect@1.9.0"
        "object-is@1.1.4"
        "object-keys@1.1.1"
        "object-visit@1.0.1"
        "object.assign@4.1.2"
        "object.pick@1.3.0"
        "omggif@1.0.10"
        "on-finished@2.3.0"
        "on-headers@1.0.2"
        "once@1.4.0"
        "onetime@2.0.1"
        "open@6.4.0"
        "optimism@0.14.0"
        "options@0.0.6"
        "ora@3.4.0"
        "os-tmpdir@1.0.2"
        "p-finally@1.0.0"
        "p-limit@3.1.0"
        "p-locate@5.0.0"
        "p-try@2.2.0"
        "pako@1.0.11"
        "parse-bmfont-ascii@1.0.6"
        "parse-bmfont-binary@1.0.6"
        "parse-bmfont-xml@1.1.4"
        "parse-headers@2.0.3"
        "parse-json@5.2.0"
        "parse-node-version@1.0.1"
        "parse-png@2.1.0"
        "parseurl@1.3.3"
        "pascalcase@0.1.1"
        "path-browserify@1.0.1"
        "path-exists@4.0.0"
        "path-extra@1.0.3"
        "path-is-absolute@1.0.1"
        "path-key@2.0.1"
        "path-parse@1.0.6"
        "path-to-regexp@1.8.0"
        "path-type@3.0.0"
        "phin@2.9.3"
        "pify@3.0.0"
        "pino-std-serializers@2.5.0"
        "pino@4.17.6"
        "pirates@4.0.1"
        "pixelmatch@4.0.2"
        "pkg-dir@3.0.0"
        "pkg-up@2.0.0"
        "plist@3.0.1"
        "plugin-error@0.1.2"
        "pngjs@5.0.0"
        "posix-character-classes@0.1.1"
        "pouchdb-collections@1.0.1"
        "prepend-http@2.0.0"
        "pretty-format@26.6.2"
        "process-nextick-args@2.0.1"
        "process@0.11.10"
        "promise@7.3.1"
        "prop-types@15.7.2"
        "pseudomap@1.0.2"
        "pump@3.0.0"
        "qs@6.9.6"
        "query-string@5.1.1"
        "querystringify@2.2.0"
        "quick-format-unescaped@1.1.2"
        "quick-lru@1.1.0"
        "range-parser@1.2.1"
        "react-devtools-core@4.10.1"
        "react-is@16.13.1"
        "react-native-iphone-x-helper@1.3.1"
        "react-native-safe-area-context@3.1.9"
        "react-refresh@0.4.3"
        "react-router@5.2.0"
        "read-pkg-up@7.0.1"
        "read-pkg@5.2.0"
        "readable-stream@3.6.0"
        "redent@2.0.0"
        "reduce-flatten@2.0.0"
        "regenerate-unicode-properties@8.2.0"
        "regenerate@1.4.2"
        "regenerator-runtime@0.13.7"
        "regenerator-transform@0.14.5"
        "regex-not@1.0.2"
        "regexp.prototype.flags@1.3.1"
        "regexpu-core@4.7.1"
        "regjsgen@0.5.2"
        "regjsparser@0.6.7"
        "remove-trailing-separator@1.1.0"
        "repeat-element@1.1.3"
        "repeat-string@1.6.1"
        "require-directory@2.1.1"
        "require-from-string@2.0.2"
        "require-main-filename@2.0.0"
        "require-resolve@0.0.2"
        "requires-port@1.0.0"
        "reselect@3.0.1"
        "resolve-from@5.0.0"
        "resolve-pathname@3.0.0"
        "resolve-url@0.2.1"
        "resolve@1.19.0"
        "restore-cursor@2.0.0"
        "ret@0.1.15"
        "rimraf@2.7.1"
        "rsvp@4.8.5"
        "rtl-detect@1.0.2"
        "run-async@2.4.1"
        "run-parallel@1.1.10"
        "rx-lite-aggregates@4.0.8"
        "rx-lite@4.0.8"
        "rxjs@5.5.12"
        "safe-buffer@5.1.2"
        "safe-regex@1.1.0"
        "safer-buffer@2.1.2"
        "sane@4.1.0"
        "sax@1.2.4"
        "scheduler@0.19.1"
        "semver@7.3.2"
        "send@0.17.1"
        "serialize-error@2.1.0"
        "serve-static@1.14.1"
        "set-blocking@2.0.0"
        "set-value@2.0.1"
        "setimmediate@1.0.5"
        "setprototypeof@1.1.1"
        "shebang-command@1.2.0"
        "shebang-regex@1.0.0"
        "shell-quote@1.6.1"
        "side-channel@1.0.4"
        "signal-exit@3.0.3"
        "simple-plist@1.1.1"
        "simple-swizzle@0.2.2"
        "slash@3.0.0"
        "slice-ansi@2.1.0"
        "slide@1.1.6"
        "slugify@1.4.6"
        "snapdragon-node@2.1.1"
        "snapdragon-util@3.0.1"
        "snapdragon@0.8.2"
        "sort-keys@2.0.0"
        "source-map-resolve@0.5.3"
        "source-map-support@0.5.19"
        "source-map-url@0.4.1"
        "source-map@0.5.7"
        "spdx-correct@3.1.1"
        "spdx-exceptions@2.3.0"
        "spdx-expression-parse@3.0.1"
        "spdx-license-ids@3.0.7"
        "split-string@3.1.0"
        "split2@2.2.0"
        "sprintf-js@1.0.3"
        "stack-generator@2.0.5"
        "stack-utils@1.0.4"
        "stackframe@1.2.0"
        "stacktrace-parser@0.1.10"
        "static-extend@0.1.2"
        "statuses@1.5.0"
        "stream-buffers@2.2.0"
        "strict-uri-encode@1.1.0"
        "string-width@4.2.0"
        "string.prototype.trimend@1.0.3"
        "string.prototype.trimstart@1.0.3"
        "string_decoder@1.3.0"
        "strip-ansi@5.2.0"
        "strip-bom@3.0.0"
        "strip-eof@1.0.0"
        "strip-indent@2.0.0"
        "sudo-prompt@9.2.1"
        "supports-color@5.5.0"
        "symbol-observable@2.0.3"
        "table-layout@1.0.1"
        "temp-dir@1.0.0"
        "temp@0.8.3"
        "tempy@0.3.0"
        "throat@4.1.0"
        "through2@2.0.5"
        "through@2.3.8"
        "time-stamp@1.1.0"
        "timm@1.7.1"
        "tiny-invariant@1.1.0"
        "tiny-queue@0.2.1"
        "tiny-warning@1.0.3"
        "tinycolor2@1.4.2"
        "tmp@0.0.33"
        "tmpl@1.0.4"
        "to-fast-properties@2.0.0"
        "to-object-path@0.3.0"
        "to-regex-range@2.1.1"
        "to-regex@3.0.2"
        "toidentifier@1.0.0"
        "trim-newlines@2.0.0"
        "ts-invariant@0.6.0"
        "tslib@1.14.1"
        "type-fest@0.3.1"
        "typedarray@0.0.6"
        "typical@4.0.0"
        "ua-parser-js@0.7.23"
        "uglify-es@3.3.9"
        "ultron@1.0.2"
        "unicode-canonical-property-names-ecmascript@1.0.4"
        "unicode-match-property-ecmascript@1.0.4"
        "unicode-match-property-value-ecmascript@1.2.0"
        "unicode-property-aliases-ecmascript@1.1.0"
        "unimodules-app-loader@1.4.0"
        "unimodules-barcode-scanner-interface@5.4.0"
        "unimodules-camera-interface@5.4.0"
        "unimodules-constants-interface@5.4.0"
        "unimodules-face-detector-interface@5.4.0"
        "unimodules-file-system-interface@5.4.0"
        "unimodules-font-interface@5.4.0"
        "unimodules-image-loader-interface@5.4.0"
        "unimodules-permissions-interface@5.4.0"
        "unimodules-sensors-interface@5.4.0"
        "unimodules-task-manager-interface@5.4.0"
        "union-value@1.0.1"
        "unique-string@1.0.0"
        "universalify@1.0.0"
        "unpipe@1.0.0"
        "unset-value@1.0.0"
        "urix@0.1.0"
        "url-parse@1.4.7"
        "use-subscription@1.5.1"
        "use@3.1.1"
        "utif@2.0.1"
        "util-deprecate@1.0.2"
        "util@0.12.3"
        "utils-merge@1.0.1"
        "uuid@3.4.0"
        "validate-npm-package-license@3.0.4"
        "value-equal@1.0.1"
        "vary@1.1.2"
        "vlq@1.0.1"
        "void-elements@2.0.1"
        "walker@1.0.7"
        "wcwidth@1.0.1"
        "whatwg-fetch@3.5.0"
        "which-boxed-primitive@1.0.2"
        "which-collection@1.0.1"
        "which-module@2.0.0"
        "which-typed-array@1.1.4"
        "which@1.3.1"
        "wordwrap@1.0.0"
        "wordwrapjs@4.0.0"
        "wrap-ansi@6.2.0"
        "wrappy@1.0.2"
        "write-file-atomic@2.4.3"
        "ws@1.1.5"
        "x-path@0.0.2"
        "xcode@2.1.0"
        "xhr@2.6.0"
        "xml-js@1.6.11"
        "xml-parse-from-string@1.0.1"
        "xml2js@0.4.23"
        "xmlbuilder@9.0.7"
        "xmldoc@1.1.2"
        "xmldom@0.1.31"
        "xpipe@1.0.5"
        "xtend@4.0.2"
        "y18n@4.0.1"
        "yallist@2.1.2"
        "yargs-parser@18.1.3"
        "yargs@15.4.1"
        "yocto-queue@0.1.0"
        "zen-observable@0.8.15"
      ];
    };
  };
in
makeDerivation {
  builder = path "/makes/packages/integrates/mobile/config/runtime/builder.sh";
  envBashLibCommon = path "/makes/utils/common/template.sh";
  envNodeRequirements = nodeRequirements;
  name = "integrates-mobile-config-runtime";
}
