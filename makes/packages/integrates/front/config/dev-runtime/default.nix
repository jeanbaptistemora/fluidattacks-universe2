{ buildNodeRequirements
, getPackageJsonDeps
, nix
, nixpkgs
, ...
}:
let
  packageJsonDeps = getPackageJsonDeps "/integrates/front/package.json";
in
buildNodeRequirements {
  name = "integrates-front-dev-runtime";
  node = nixpkgs.nodejs-12_x;
  requirements = {
    direct = nix.sort (packageJsonDeps.development ++ packageJsonDeps.production);
    inherited = [
      "@ant-design/colors@6.0.0"
      "@ant-design/icons-svg@4.1.0"
      "@ant-design/icons@4.6.2"
      "@ant-design/react-slick@0.28.2"
      "@babel/code-frame@7.12.13"
      "@babel/core@7.12.13"
      "@babel/generator@7.12.15"
      "@babel/helper-annotate-as-pure@7.12.13"
      "@babel/helper-function-name@7.12.13"
      "@babel/helper-get-function-arity@7.12.13"
      "@babel/helper-member-expression-to-functions@7.12.13"
      "@babel/helper-module-imports@7.12.13"
      "@babel/helper-module-transforms@7.12.13"
      "@babel/helper-optimise-call-expression@7.12.13"
      "@babel/helper-plugin-utils@7.12.13"
      "@babel/helper-replace-supers@7.12.13"
      "@babel/helper-simple-access@7.12.13"
      "@babel/helper-split-export-declaration@7.12.13"
      "@babel/helper-validator-identifier@7.12.11"
      "@babel/helpers@7.12.13"
      "@babel/highlight@7.12.13"
      "@babel/parser@7.12.15"
      "@babel/plugin-syntax-async-generators@7.8.4"
      "@babel/plugin-syntax-bigint@7.8.3"
      "@babel/plugin-syntax-class-properties@7.12.13"
      "@babel/plugin-syntax-import-meta@7.10.4"
      "@babel/plugin-syntax-json-strings@7.8.3"
      "@babel/plugin-syntax-logical-assignment-operators@7.10.4"
      "@babel/plugin-syntax-nullish-coalescing-operator@7.8.3"
      "@babel/plugin-syntax-numeric-separator@7.10.4"
      "@babel/plugin-syntax-object-rest-spread@7.8.3"
      "@babel/plugin-syntax-optional-catch-binding@7.8.3"
      "@babel/plugin-syntax-optional-chaining@7.8.3"
      "@babel/plugin-syntax-top-level-await@7.12.13"
      "@babel/runtime-corejs2@7.12.13"
      "@babel/runtime-corejs3@7.12.13"
      "@babel/runtime@7.12.13"
      "@babel/template@7.12.13"
      "@babel/traverse@7.12.13"
      "@babel/types@7.12.13"
      "@bcoe/v8-coverage@0.2.3"
      "@bugsnag/browser@7.6.0"
      "@bugsnag/cuid@3.0.0"
      "@bugsnag/node@7.6.0"
      "@bugsnag/safe-json-stringify@6.0.0"
      "@cnakazawa/watch@1.0.4"
      "@ctrl/tinycolor@3.4.0"
      "@discoveryjs/json-ext@0.5.3"
      "@emotion/is-prop-valid@0.8.8"
      "@emotion/memoize@0.7.4"
      "@emotion/stylis@0.8.5"
      "@emotion/unitless@0.7.5"
      "@eslint/eslintrc@0.2.2"
      "@fortawesome/fontawesome-common-types@0.2.34"
      "@graphql-typed-document-node/core@3.1.0"
      "@istanbuljs/load-nyc-config@1.1.0"
      "@istanbuljs/schema@0.1.2"
      "@jest/console@26.6.2"
      "@jest/core@26.6.3"
      "@jest/environment@26.6.2"
      "@jest/fake-timers@26.6.2"
      "@jest/globals@26.6.2"
      "@jest/reporters@26.6.2"
      "@jest/source-map@26.6.2"
      "@jest/test-result@26.6.2"
      "@jest/test-sequencer@26.6.3"
      "@jest/transform@26.6.2"
      "@jest/types@26.6.2"
      "@nodelib/fs.scandir@2.1.4"
      "@nodelib/fs.stat@2.0.4"
      "@nodelib/fs.walk@1.2.6"
      "@npmcli/move-file@1.1.1"
      "@sinonjs/commons@1.8.2"
      "@sinonjs/fake-timers@6.0.1"
      "@stylelint/postcss-css-in-js@0.37.2"
      "@stylelint/postcss-markdown@0.36.2"
      "@tanem/svg-injector@8.2.3"
      "@trysound/sax@0.1.1"
      "@types/anymatch@1.3.1"
      "@types/babel__core@7.1.12"
      "@types/babel__generator@7.6.2"
      "@types/babel__template@7.4.0"
      "@types/babel__traverse@7.11.0"
      "@types/body-parser@1.19.0"
      "@types/cheerio@0.22.23"
      "@types/connect-history-api-fallback@1.3.3"
      "@types/connect@3.4.34"
      "@types/css-modules-loader-core@1.1.0"
      "@types/cssnano@4.0.0"
      "@types/eslint-scope@3.7.0"
      "@types/eslint@7.2.10"
      "@types/estree@0.0.47"
      "@types/express-serve-static-core@4.17.18"
      "@types/express@4.17.11"
      "@types/extract-files@8.1.0"
      "@types/glob@7.1.3"
      "@types/graceful-fs@4.1.4"
      "@types/hast@2.3.1"
      "@types/history@4.7.8"
      "@types/hoist-non-react-statics@3.3.1"
      "@types/http-proxy-middleware@0.19.3"
      "@types/http-proxy@1.17.5"
      "@types/invariant@2.2.34"
      "@types/istanbul-lib-coverage@2.0.3"
      "@types/istanbul-lib-report@3.0.0"
      "@types/istanbul-reports@3.0.0"
      "@types/json-schema@7.0.7"
      "@types/json5@0.0.29"
      "@types/mdast@3.0.3"
      "@types/mime@1.3.2"
      "@types/minimatch@3.0.3"
      "@types/minimist@1.2.1"
      "@types/node@14.14.25"
      "@types/normalize-package-data@2.4.0"
      "@types/parse-json@4.0.0"
      "@types/parse5@6.0.0"
      "@types/prettier@2.2.1"
      "@types/prop-types@15.7.3"
      "@types/q@1.5.4"
      "@types/qs@6.9.5"
      "@types/range-parser@1.2.3"
      "@types/redux@3.6.0"
      "@types/serve-static@1.13.9"
      "@types/sizzle@2.3.2"
      "@types/source-list-map@0.1.2"
      "@types/stack-utils@2.0.0"
      "@types/tapable@1.0.6"
      "@types/tough-cookie@4.0.0"
      "@types/uglify-js@3.12.0"
      "@types/unist@2.0.3"
      "@types/webpack-sources@2.1.0"
      "@types/webpack@5.28.0"
      "@types/yargs-parser@20.2.0"
      "@types/yargs@15.0.13"
      "@types/zen-observable@0.8.2"
      "@typescript-eslint/experimental-utils@4.15.2"
      "@typescript-eslint/scope-manager@4.15.2"
      "@typescript-eslint/types@4.15.2"
      "@typescript-eslint/typescript-estree@4.15.2"
      "@typescript-eslint/visitor-keys@4.15.2"
      "@webassemblyjs/ast@1.9.0"
      "@webassemblyjs/floating-point-hex-parser@1.9.0"
      "@webassemblyjs/helper-api-error@1.9.0"
      "@webassemblyjs/helper-buffer@1.9.0"
      "@webassemblyjs/helper-code-frame@1.9.0"
      "@webassemblyjs/helper-fsm@1.9.0"
      "@webassemblyjs/helper-module-context@1.9.0"
      "@webassemblyjs/helper-numbers@1.11.0"
      "@webassemblyjs/helper-wasm-bytecode@1.9.0"
      "@webassemblyjs/helper-wasm-section@1.9.0"
      "@webassemblyjs/ieee754@1.9.0"
      "@webassemblyjs/leb128@1.9.0"
      "@webassemblyjs/utf8@1.9.0"
      "@webassemblyjs/wasm-edit@1.9.0"
      "@webassemblyjs/wasm-gen@1.9.0"
      "@webassemblyjs/wasm-opt@1.9.0"
      "@webassemblyjs/wasm-parser@1.9.0"
      "@webassemblyjs/wast-parser@1.9.0"
      "@webassemblyjs/wast-printer@1.9.0"
      "@webpack-cli/configtest@1.0.3"
      "@webpack-cli/info@1.2.2"
      "@webpack-cli/serve@1.3.0"
      "@wry/context@0.4.4"
      "@wry/equality@0.1.11"
      "@wry/trie@0.3.0"
      "@xtuc/ieee754@1.2.0"
      "@xtuc/long@4.2.2"
      "abab@2.0.5"
      "accepts@1.3.7"
      "acorn-globals@6.0.0"
      "acorn-jsx@5.3.1"
      "acorn-walk@7.2.0"
      "acorn@7.4.1"
      "aggregate-error@3.1.0"
      "airbnb-prop-types@2.16.0"
      "ajv-errors@1.0.1"
      "ajv-keywords@3.5.2"
      "ajv@6.12.6"
      "alphanum-sort@1.0.2"
      "amdefine@1.0.1"
      "ansi-colors@4.1.1"
      "ansi-escapes@4.3.1"
      "ansi-html@0.0.7"
      "ansi-regex@5.0.0"
      "ansi-styles@3.2.1"
      "anymatch@3.1.1"
      "apollo-cache@1.3.5"
      "apollo-utilities@1.3.4"
      "aproba@1.2.0"
      "arg@4.1.3"
      "argparse@1.0.10"
      "aria-query@4.2.2"
      "arr-diff@4.0.0"
      "arr-flatten@1.1.0"
      "arr-union@3.1.0"
      "array-back@4.0.1"
      "array-filter@1.0.0"
      "array-find-index@1.0.2"
      "array-flatten@2.1.2"
      "array-includes@3.1.2"
      "array-tree-filter@2.1.0"
      "array-union@2.1.0"
      "array-uniq@1.0.3"
      "array-unique@0.3.2"
      "array.prototype.find@2.1.1"
      "array.prototype.flat@1.2.4"
      "array.prototype.flatmap@1.2.4"
      "arrify@1.0.1"
      "asap@2.0.6"
      "asn1.js@5.4.1"
      "asn1@0.2.4"
      "assert-plus@1.0.0"
      "assert@1.5.0"
      "assign-symbols@1.0.0"
      "ast-transform@0.0.0"
      "ast-types-flow@0.0.7"
      "ast-types@0.7.8"
      "astral-regex@1.0.0"
      "async-each@1.0.3"
      "async-limiter@1.0.1"
      "async-validator@3.5.1"
      "async@2.6.3"
      "asynckit@0.4.0"
      "atob@2.1.2"
      "autobind-decorator@2.4.0"
      "autoprefixer@9.8.6"
      "aws-sign2@0.7.0"
      "aws4@1.11.0"
      "axe-core@4.1.2"
      "axobject-query@2.2.0"
      "babel-jest@26.6.3"
      "babel-plugin-istanbul@6.0.0"
      "babel-plugin-jest-hoist@26.6.2"
      "babel-plugin-styled-components@1.12.0"
      "babel-plugin-syntax-jsx@6.18.0"
      "babel-preset-current-node-syntax@1.0.1"
      "babel-preset-jest@26.6.2"
      "babel-runtime@6.26.0"
      "backo2@1.0.2"
      "bail@1.0.5"
      "balanced-match@1.0.0"
      "base64-js@1.5.1"
      "base@0.11.2"
      "batch@0.6.1"
      "bcrypt-pbkdf@1.0.2"
      "big.js@5.2.2"
      "binary-extensions@2.2.0"
      "bindings@1.5.0"
      "bluebird@3.7.2"
      "bn.js@5.1.3"
      "body-parser@1.19.0"
      "bonjour@3.5.0"
      "boolbase@1.0.0"
      "brace-expansion@1.1.11"
      "braces@3.0.2"
      "brorand@1.1.0"
      "browser-process-hrtime@1.0.0"
      "browser-resolve@1.11.3"
      "browserify-aes@1.2.0"
      "browserify-cipher@1.0.1"
      "browserify-des@1.0.2"
      "browserify-optional@1.0.1"
      "browserify-rsa@4.1.0"
      "browserify-sign@4.2.1"
      "browserify-zlib@0.2.0"
      "browserslist@4.16.3"
      "bs-logger@0.2.6"
      "bser@2.1.1"
      "buffer-from@1.1.1"
      "buffer-indexof@1.1.1"
      "buffer-xor@1.0.3"
      "buffer@4.9.2"
      "bugsnag-build-reporter@1.0.3"
      "bugsnag-sourcemaps@1.3.0"
      "builtin-modules@1.1.1"
      "builtin-status-codes@3.0.0"
      "byline@5.0.0"
      "bytes@3.0.0"
      "cacache@15.0.5"
      "cache-base@1.0.1"
      "call-bind@1.0.2"
      "caller-callsite@2.0.0"
      "caller-path@2.0.0"
      "callsites@3.1.0"
      "camelcase-keys@6.2.2"
      "camelcase@6.2.0"
      "camelize@1.0.0"
      "caniuse-api@3.0.0"
      "caniuse-lite@1.0.30001185"
      "capture-exit@2.0.0"
      "caseless@0.12.0"
      "chalk@2.4.2"
      "change-emitter@0.1.6"
      "char-regex@1.0.2"
      "character-entities-legacy@1.1.4"
      "character-entities@1.2.4"
      "character-reference-invalid@1.1.4"
      "chartjs-color-string@0.6.0"
      "chartjs-color@2.4.1"
      "chokidar@3.5.1"
      "chownr@2.0.0"
      "chrome-trace-event@1.0.2"
      "ci-info@2.0.0"
      "cipher-base@1.0.4"
      "cjs-module-lexer@0.6.0"
      "class-utils@0.3.6"
      "classnames@2.2.6"
      "clean-stack@2.2.0"
      "clipboard@2.0.6"
      "cliui@6.0.0"
      "clone-deep@4.0.1"
      "clone-regexp@2.2.0"
      "clsx@1.1.1"
      "co@4.6.0"
      "coa@2.0.2"
      "collect-v8-coverage@1.0.1"
      "collection-visit@1.0.0"
      "color-convert@1.9.3"
      "color-name@1.1.4"
      "color-string@1.5.4"
      "color@3.1.3"
      "colord@1.7.1"
      "colorette@1.2.1"
      "combined-stream@1.0.8"
      "comma-separated-tokens@1.0.8"
      "command-line-usage@6.1.1"
      "commander@2.20.3"
      "commondir@1.0.1"
      "component-emitter@1.3.0"
      "compressible@2.0.18"
      "compression@1.7.4"
      "compute-scroll-into-view@1.0.17"
      "concat-map@0.0.1"
      "concat-stream@1.6.2"
      "connect-history-api-fallback@1.6.0"
      "console-browserify@1.2.0"
      "constants-browserify@1.0.0"
      "contains-path@0.1.0"
      "content-disposition@0.5.3"
      "content-type@1.0.4"
      "convert-source-map@1.7.0"
      "cookie-signature@1.0.6"
      "cookie@0.4.0"
      "copy-concurrently@1.0.5"
      "copy-descriptor@0.1.1"
      "copy-to-clipboard@3.3.1"
      "core-js-pure@3.8.3"
      "core-js@2.6.12"
      "core-util-is@1.0.2"
      "cosmiconfig@5.2.1"
      "create-ecdh@4.0.4"
      "create-eslint-index@1.0.0"
      "create-hash@1.2.0"
      "create-hmac@1.1.7"
      "create-react-class@15.7.0"
      "create-require@1.1.1"
      "cross-spawn@7.0.3"
      "css-color-keywords@1.0.0"
      "css-color-names@0.0.4"
      "css-declaration-sorter@4.0.1"
      "css-modules-loader-core@1.1.0"
      "css-select-base-adapter@0.1.1"
      "css-select@1.2.0"
      "css-selector-tokenizer@0.7.3"
      "css-to-react-native@3.0.0"
      "css-tree@1.0.0-alpha.37"
      "css-what@2.1.3"
      "cssesc@3.0.0"
      "cssfontparser@1.2.1"
      "cssnano-preset-default@4.0.7"
      "cssnano-util-get-arguments@4.0.0"
      "cssnano-util-get-match@4.0.0"
      "cssnano-util-raw-cache@4.0.1"
      "cssnano-util-same-parent@4.0.1"
      "cssnano-utils@2.0.0"
      "cssnano@4.1.10"
      "csso@4.2.0"
      "cssom@0.4.4"
      "cssstyle@2.3.0"
      "csstype@3.0.6"
      "currently-unhandled@0.4.1"
      "cyclist@1.0.1"
      "damerau-levenshtein@1.0.6"
      "dashdash@1.14.1"
      "data-urls@2.0.0"
      "date-fns@2.19.0"
      "debug@4.3.1"
      "decamelize-keys@1.1.0"
      "decamelize@1.2.0"
      "decimal.js@10.2.1"
      "decode-uri-component@0.2.0"
      "deep-equal@1.1.1"
      "deep-extend@0.6.0"
      "deep-is@0.1.3"
      "deepmerge@4.2.2"
      "default-gateway@4.2.0"
      "define-properties@1.1.3"
      "define-property@2.0.2"
      "del@4.1.1"
      "delayed-stream@1.0.0"
      "delegate@3.2.0"
      "depd@1.1.2"
      "des.js@1.0.1"
      "destroy@1.0.4"
      "detect-newline@3.1.0"
      "detect-node@2.0.4"
      "detect-passive-events@1.0.5"
      "diff-sequences@26.6.2"
      "diff@4.0.2"
      "diffie-hellman@5.0.3"
      "dir-glob@3.0.1"
      "discontinuous-range@1.0.0"
      "dnd-core@4.0.5"
      "dns-equal@1.0.0"
      "dns-packet@1.3.1"
      "dns-txt@2.0.2"
      "doctrine@3.0.0"
      "dom-align@1.12.0"
      "dom-helpers@3.4.0"
      "dom-serializer@0.1.1"
      "domain-browser@1.2.0"
      "domelementtype@1.3.1"
      "domexception@2.0.1"
      "domhandler@2.4.2"
      "domutils@1.5.1"
      "dot-prop@5.3.0"
      "duplexify@3.7.1"
      "ecc-jsbn@0.1.2"
      "ee-first@1.1.1"
      "electron-to-chromium@1.3.659"
      "elliptic@6.5.4"
      "emittery@0.7.2"
      "emoji-regex@7.0.3"
      "emojis-list@3.0.0"
      "encodeurl@1.0.2"
      "encoding@0.1.13"
      "end-of-stream@1.4.4"
      "enhanced-resolve@4.5.0"
      "enquirer@2.3.6"
      "entities@1.1.2"
      "envinfo@7.7.4"
      "enzyme-adapter-utils@1.14.0"
      "enzyme-shallow-equal@1.0.4"
      "errno@0.1.8"
      "error-ex@1.3.2"
      "error-stack-parser@2.0.6"
      "es-abstract@1.18.0-next.2"
      "es-module-lexer@0.4.1"
      "es-to-primitive@1.2.1"
      "es6-error@4.1.1"
      "escalade@3.1.1"
      "escape-html@1.0.3"
      "escape-string-regexp@1.0.5"
      "escodegen@1.14.3"
      "eslint-ast-utils@1.1.0"
      "eslint-import-resolver-node@0.3.4"
      "eslint-module-utils@2.6.0"
      "eslint-scope@5.1.1"
      "eslint-utils@2.1.0"
      "eslint-visitor-keys@2.0.0"
      "espree@7.3.1"
      "esprima@4.0.1"
      "esquery@1.4.0"
      "esrecurse@4.3.0"
      "estraverse@4.3.0"
      "esutils@2.0.3"
      "etag@1.8.1"
      "eve@0.5.4"
      "eventemitter3@3.1.2"
      "events@3.2.0"
      "eventsource@1.0.7"
      "evp_bytestokey@1.0.3"
      "exec-sh@0.3.4"
      "execa@1.0.0"
      "execall@2.0.0"
      "exenv@1.2.2"
      "exit@0.1.2"
      "expand-brackets@2.1.4"
      "expect@26.6.2"
      "express@4.17.1"
      "extend-shallow@3.0.2"
      "extend@3.0.2"
      "extglob@2.0.4"
      "extract-files@8.1.0"
      "extsprintf@1.3.0"
      "fast-deep-equal@3.1.3"
      "fast-diff@1.2.0"
      "fast-glob@3.2.5"
      "fast-json-parse@1.0.3"
      "fast-json-stable-stringify@2.1.0"
      "fast-levenshtein@2.0.6"
      "fast-safe-stringify@1.2.3"
      "fastest-levenshtein@1.0.12"
      "fastparse@1.1.2"
      "fastq@1.10.1"
      "fault@1.0.4"
      "faye-websocket@0.10.0"
      "fb-watchman@2.0.1"
      "fbjs@0.8.17"
      "figgy-pudding@3.5.2"
      "file-entry-cache@5.0.1"
      "file-saver@2.0.2"
      "file-uri-to-path@1.0.0"
      "fill-range@7.0.1"
      "finalhandler@1.1.2"
      "find-cache-dir@3.3.1"
      "find-nearest-file@1.1.0"
      "find-up@2.1.0"
      "flat-cache@2.0.1"
      "flatstr@1.0.12"
      "flatted@2.0.2"
      "flush-write-stream@1.1.1"
      "follow-redirects@1.13.2"
      "for-in@1.0.2"
      "forever-agent@0.6.1"
      "form-data@2.3.3"
      "format@0.2.2"
      "forwarded@0.1.2"
      "fragment-cache@0.2.1"
      "fresh@0.5.2"
      "from2@2.3.0"
      "fs-minipass@2.1.0"
      "fs-write-stream-atomic@1.0.10"
      "fs.realpath@1.0.0"
      "fsevents@2.3.2"
      "function-bind@1.1.1"
      "function.prototype.name@1.1.3"
      "functional-red-black-tree@1.0.1"
      "functions-have-names@1.2.2"
      "gensync@1.0.0-beta.2"
      "get-caller-file@2.0.5"
      "get-intrinsic@1.1.1"
      "get-package-type@0.1.0"
      "get-stdin@6.0.0"
      "get-stream@4.1.0"
      "get-value@2.0.6"
      "getpass@0.1.7"
      "glob-parent@5.1.1"
      "glob-to-regexp@0.4.1"
      "glob@7.1.6"
      "global-modules@2.0.0"
      "global-prefix@3.0.0"
      "globals@11.12.0"
      "globby@11.0.2"
      "globjoin@0.1.4"
      "gonzales-pe@4.3.0"
      "good-listener@1.2.2"
      "graceful-fs@4.2.4"
      "graphql-tag@2.12.3"
      "growly@1.3.0"
      "handle-thing@2.0.1"
      "har-schema@2.0.0"
      "har-validator@5.1.5"
      "hard-rejection@2.1.0"
      "harmony-reflect@1.6.1"
      "has-ansi@2.0.0"
      "has-bigints@1.0.1"
      "has-flag@3.0.0"
      "has-symbols@1.0.1"
      "has-value@1.0.0"
      "has-values@1.0.0"
      "has@1.0.3"
      "hash-base@3.1.0"
      "hash.js@1.1.7"
      "hast-util-parse-selector@2.2.5"
      "hastscript@6.0.0"
      "hex-color-regex@1.1.0"
      "highlight.js@10.6.0"
      "history@4.10.1"
      "hmac-drbg@1.0.1"
      "hoist-non-react-statics@3.3.2"
      "hosted-git-info@2.8.8"
      "hpack.js@2.1.6"
      "hsl-regex@1.0.0"
      "hsla-regex@1.0.0"
      "html-comment-regex@1.1.2"
      "html-element-map@1.3.0"
      "html-encoding-sniffer@2.0.1"
      "html-entities@1.4.0"
      "html-escaper@2.0.2"
      "html-parse-stringify2@2.0.1"
      "html-tags@3.1.0"
      "htmlparser2@3.10.1"
      "http-deceiver@1.2.7"
      "http-errors@1.7.2"
      "http-parser-js@0.5.3"
      "http-proxy-middleware@0.19.1"
      "http-proxy@1.18.1"
      "http-signature@1.2.0"
      "https-browserify@1.0.0"
      "human-signals@1.1.1"
      "iconv-lite@0.4.24"
      "icss-replace-symbols@1.1.0"
      "icss-utils@5.1.0"
      "ieee754@1.2.1"
      "iferr@0.1.5"
      "ignore@5.1.8"
      "import-fresh@3.3.0"
      "import-lazy@4.0.0"
      "import-local@3.0.2"
      "imurmurhash@0.1.4"
      "indent-string@4.0.0"
      "indexes-of@1.0.1"
      "infer-owner@1.0.4"
      "inflight@1.0.6"
      "inherits@2.0.4"
      "ini@1.3.8"
      "internal-ip@4.3.0"
      "internal-slot@1.0.3"
      "interpret@2.2.0"
      "invariant@2.2.4"
      "ip-regex@2.1.0"
      "ip@1.1.5"
      "ipaddr.js@1.9.1"
      "is-absolute-url@2.1.0"
      "is-accessor-descriptor@0.1.6"
      "is-alphabetical@1.0.4"
      "is-alphanumerical@1.0.4"
      "is-arguments@1.1.0"
      "is-arrayish@0.2.1"
      "is-bigint@1.0.1"
      "is-binary-path@2.1.0"
      "is-boolean-object@1.1.0"
      "is-buffer@1.1.6"
      "is-callable@1.2.3"
      "is-ci@2.0.0"
      "is-color-stop@1.1.0"
      "is-core-module@2.2.0"
      "is-data-descriptor@0.1.4"
      "is-date-object@1.0.2"
      "is-decimal@1.0.4"
      "is-descriptor@0.1.6"
      "is-directory@0.3.1"
      "is-docker@2.1.1"
      "is-extendable@0.1.1"
      "is-extglob@2.1.1"
      "is-finite@1.1.0"
      "is-fullwidth-code-point@2.0.0"
      "is-generator-fn@2.1.0"
      "is-glob@4.0.1"
      "is-hexadecimal@1.0.4"
      "is-negative-zero@2.0.1"
      "is-number-object@1.0.4"
      "is-number@7.0.0"
      "is-obj@2.0.0"
      "is-path-cwd@2.2.0"
      "is-path-in-cwd@2.1.0"
      "is-path-inside@2.1.0"
      "is-plain-obj@2.1.0"
      "is-plain-object@2.0.4"
      "is-potential-custom-element-name@1.0.0"
      "is-promise@2.2.2"
      "is-regex@1.1.2"
      "is-regexp@2.1.0"
      "is-resolvable@1.1.0"
      "is-stream@1.1.0"
      "is-string@1.0.5"
      "is-subset@0.1.1"
      "is-svg@3.0.0"
      "is-symbol@1.0.3"
      "is-there@4.5.1"
      "is-typedarray@1.0.0"
      "is-utf8@0.2.1"
      "is-windows@1.0.2"
      "is-wsl@2.2.0"
      "isarray@0.0.1"
      "iserror@0.0.2"
      "isexe@2.0.0"
      "isobject@3.0.1"
      "isomorphic-fetch@2.2.1"
      "isstream@0.1.2"
      "istanbul-lib-coverage@3.0.0"
      "istanbul-lib-instrument@4.0.3"
      "istanbul-lib-report@3.0.0"
      "istanbul-lib-source-maps@4.0.0"
      "istanbul-reports@3.0.2"
      "iterall@1.3.0"
      "jest-changed-files@26.6.2"
      "jest-config@26.6.3"
      "jest-diff@26.6.2"
      "jest-docblock@26.0.0"
      "jest-each@26.6.2"
      "jest-environment-jsdom@26.6.2"
      "jest-environment-node@26.6.2"
      "jest-get-type@26.3.0"
      "jest-haste-map@26.6.2"
      "jest-jasmine2@26.6.3"
      "jest-leak-detector@26.6.2"
      "jest-matcher-utils@26.6.2"
      "jest-message-util@26.6.2"
      "jest-mock@26.6.2"
      "jest-pnp-resolver@1.2.2"
      "jest-regex-util@26.0.0"
      "jest-resolve-dependencies@26.6.3"
      "jest-resolve@26.6.2"
      "jest-runner@26.6.3"
      "jest-runtime@26.6.3"
      "jest-serializer@26.6.2"
      "jest-snapshot@26.6.2"
      "jest-util@26.6.2"
      "jest-validate@26.6.2"
      "jest-watcher@26.6.2"
      "jest-worker@26.6.2"
      "js-tokens@4.0.0"
      "js-yaml@3.14.1"
      "jsbn@0.1.1"
      "jsesc@2.5.2"
      "json-parse-better-errors@1.0.2"
      "json-parse-even-better-errors@2.3.1"
      "json-schema-traverse@0.4.1"
      "json-schema@0.2.3"
      "json-stable-stringify-without-jsonify@1.0.1"
      "json-stringify-safe@5.0.1"
      "json2mq@0.2.0"
      "json3@3.3.3"
      "json5@2.2.0"
      "jsprim@1.4.1"
      "jsx-ast-utils@3.2.0"
      "keycode@2.2.0"
      "killable@1.0.1"
      "kind-of@6.0.3"
      "kleur@3.0.3"
      "known-css-properties@0.20.0"
      "language-subtag-registry@0.3.21"
      "language-tags@1.0.5"
      "last-call-webpack-plugin@3.0.0"
      "leven@3.1.0"
      "levn@0.3.0"
      "lines-and-columns@1.1.6"
      "linkify-it@2.2.0"
      "load-json-file@2.0.0"
      "loader-runner@2.4.0"
      "loader-utils@2.0.0"
      "locate-path@2.0.0"
      "lodash-es@4.17.20"
      "lodash.clonedeep@4.5.0"
      "lodash.debounce@4.0.8"
      "lodash.escape@4.0.1"
      "lodash.flatten@4.4.0"
      "lodash.flattendeep@4.4.0"
      "lodash.get@4.4.2"
      "lodash.isequal@4.5.0"
      "lodash.memoize@4.1.2"
      "lodash.reduce@4.6.0"
      "lodash.sortby@4.7.0"
      "lodash.startswith@4.2.1"
      "lodash.truncate@4.4.2"
      "lodash.uniq@4.5.0"
      "lodash.zip@4.2.0"
      "log-symbols@4.0.0"
      "loglevel@1.7.1"
      "longest-streak@2.0.4"
      "loose-envify@1.4.0"
      "loud-rejection@1.6.0"
      "lowlight@1.19.0"
      "lru-cache@6.0.0"
      "make-dir@3.1.0"
      "make-error@1.3.6"
      "makeerror@1.0.11"
      "map-cache@0.2.2"
      "map-obj@4.1.0"
      "map-visit@1.0.0"
      "mathml-tag-names@2.1.3"
      "md5.js@1.3.5"
      "mdast-util-from-markdown@0.8.5"
      "mdast-util-to-markdown@0.6.5"
      "mdast-util-to-string@2.0.0"
      "mdn-data@2.0.4"
      "media-typer@0.3.0"
      "memory-fs@0.5.0"
      "meow@8.1.2"
      "merge-descriptors@1.0.1"
      "merge-stream@2.0.0"
      "merge2@1.4.1"
      "methods@1.1.2"
      "micromark@2.11.4"
      "micromatch@4.0.2"
      "miller-rabin@4.0.1"
      "mime-db@1.45.0"
      "mime-types@2.1.28"
      "mime@1.6.0"
      "mimic-fn@2.1.0"
      "min-indent@1.0.1"
      "mini-create-react-context@0.4.1"
      "mini-store@3.0.6"
      "minimalistic-assert@1.0.1"
      "minimalistic-crypto-utils@1.0.1"
      "minimatch@3.0.4"
      "minimist-options@4.1.0"
      "minimist@1.2.5"
      "minipass-collect@1.0.2"
      "minipass-flush@1.0.5"
      "minipass-pipeline@1.2.4"
      "minipass@3.1.3"
      "minizlib@2.1.2"
      "mississippi@3.0.0"
      "mixin-deep@1.3.2"
      "mkdirp@0.5.5"
      "moo-color@1.0.2"
      "moo@0.5.1"
      "move-concurrently@1.0.1"
      "ms@2.1.2"
      "multicast-dns-service-types@1.1.0"
      "multicast-dns@6.2.3"
      "nan@2.14.2"
      "nanoclone@0.2.1"
      "nanoid@3.1.20"
      "nanomatch@1.2.13"
      "native-url@0.2.6"
      "natural-compare@1.4.0"
      "nearley@2.20.1"
      "negotiator@0.6.2"
      "neo-async@2.6.2"
      "nice-try@1.0.5"
      "node-fetch@2.6.1"
      "node-forge@0.10.0"
      "node-int64@0.4.0"
      "node-libs-browser@2.2.1"
      "node-modules-regexp@1.0.0"
      "node-notifier@8.0.1"
      "node-releases@1.1.70"
      "normalize-package-data@2.5.0"
      "normalize-path@3.0.0"
      "normalize-range@0.1.2"
      "normalize-selector@0.2.0"
      "normalize-url@3.3.0"
      "npm-run-path@2.0.2"
      "nth-check@1.0.2"
      "num2fraction@1.2.2"
      "nwsapi@2.2.0"
      "oauth-sign@0.9.0"
      "object-assign@4.1.1"
      "object-copy@0.1.0"
      "object-inspect@1.9.0"
      "object-is@1.1.4"
      "object-keys@1.1.1"
      "object-visit@1.0.1"
      "object.assign@4.1.2"
      "object.entries@1.1.3"
      "object.fromentries@2.0.3"
      "object.getownpropertydescriptors@2.1.1"
      "object.pick@1.3.0"
      "object.values@1.1.2"
      "obuf@1.1.2"
      "on-finished@2.3.0"
      "on-headers@1.0.2"
      "once@1.4.0"
      "onetime@5.1.2"
      "opn@5.5.0"
      "optimism@0.10.3"
      "optionator@0.8.3"
      "original@1.0.2"
      "os-browserify@0.3.0"
      "p-each-series@2.2.0"
      "p-finally@1.0.0"
      "p-limit@1.3.0"
      "p-locate@2.0.0"
      "p-map@4.0.0"
      "p-retry@3.0.1"
      "p-try@1.0.0"
      "pako@1.0.11"
      "parallel-transform@1.2.0"
      "parent-module@1.0.1"
      "parse-asn1@5.1.6"
      "parse-entities@2.0.0"
      "parse-json@2.2.0"
      "parse5@5.1.1"
      "parseurl@1.3.3"
      "pascalcase@0.1.1"
      "path-browserify@0.0.1"
      "path-dirname@1.0.2"
      "path-exists@3.0.0"
      "path-is-absolute@1.0.1"
      "path-is-inside@1.0.2"
      "path-key@3.1.1"
      "path-parse@1.0.6"
      "path-to-regexp@1.8.0"
      "path-type@4.0.0"
      "pbkdf2@3.1.1"
      "performance-now@2.1.0"
      "picomatch@2.2.2"
      "pify@2.3.0"
      "pinkie-promise@2.0.1"
      "pinkie@2.0.4"
      "pino-std-serializers@2.5.0"
      "pino@4.17.6"
      "pirates@4.0.1"
      "pkg-dir@2.0.0"
      "portfinder@1.0.28"
      "posix-character-classes@0.1.1"
      "postcss-calc@7.0.5"
      "postcss-colormin@4.0.3"
      "postcss-convert-values@4.0.1"
      "postcss-discard-comments@4.0.2"
      "postcss-discard-duplicates@4.0.2"
      "postcss-discard-empty@4.0.1"
      "postcss-discard-overridden@4.0.1"
      "postcss-html@0.36.0"
      "postcss-less@3.1.4"
      "postcss-media-query-parser@0.2.3"
      "postcss-merge-longhand@4.0.11"
      "postcss-merge-rules@4.0.3"
      "postcss-minify-font-values@4.0.2"
      "postcss-minify-gradients@4.0.2"
      "postcss-minify-params@4.0.2"
      "postcss-minify-selectors@4.0.2"
      "postcss-modules-extract-imports@3.0.0"
      "postcss-modules-local-by-default@4.0.0"
      "postcss-modules-scope@3.0.0"
      "postcss-modules-values@4.0.0"
      "postcss-normalize-charset@4.0.1"
      "postcss-normalize-display-values@4.0.2"
      "postcss-normalize-positions@4.0.2"
      "postcss-normalize-repeat-style@4.0.2"
      "postcss-normalize-string@4.0.2"
      "postcss-normalize-timing-functions@4.0.2"
      "postcss-normalize-unicode@4.0.1"
      "postcss-normalize-url@4.0.1"
      "postcss-normalize-whitespace@4.0.2"
      "postcss-ordered-values@4.1.2"
      "postcss-reduce-initial@4.0.3"
      "postcss-reduce-transforms@4.0.2"
      "postcss-resolve-nested-selector@0.1.1"
      "postcss-safe-parser@4.0.2"
      "postcss-sass@0.4.4"
      "postcss-scss@2.1.1"
      "postcss-selector-parser@6.0.4"
      "postcss-svgo@4.0.2"
      "postcss-syntax@0.36.2"
      "postcss-unique-selectors@4.0.1"
      "postcss-value-parser@4.1.0"
      "postcss@8.2.5"
      "prelude-ls@1.1.2"
      "prettier-linter-helpers@1.0.0"
      "pretty-format@26.6.2"
      "prismjs@1.23.0"
      "process-nextick-args@2.0.1"
      "process@0.11.10"
      "progress@2.0.3"
      "promise-inflight@1.0.1"
      "promise@7.3.1"
      "prompts@2.4.0"
      "prop-types-exact@1.2.0"
      "prop-types-extra@1.1.1"
      "prop-types@15.7.2"
      "property-expr@2.0.4"
      "property-information@5.6.0"
      "proxy-addr@2.0.6"
      "prr@1.0.1"
      "psl@1.8.0"
      "public-encrypt@4.0.3"
      "pump@3.0.0"
      "pumpify@1.5.1"
      "punycode@2.1.1"
      "q@1.5.1"
      "qs@6.5.2"
      "querystring-es3@0.2.1"
      "querystring@0.2.0"
      "querystringify@2.2.0"
      "quick-format-unescaped@1.1.2"
      "quick-lru@4.0.1"
      "raf@3.4.1"
      "railroad-diagrams@1.0.0"
      "randexp@0.4.6"
      "randombytes@2.1.0"
      "randomfill@1.0.4"
      "range-parser@1.2.1"
      "raw-body@2.4.0"
      "rc-align@4.0.9"
      "rc-cascader@1.4.2"
      "rc-checkbox@2.3.2"
      "rc-collapse@3.1.0"
      "rc-dialog@8.5.2"
      "rc-drawer@4.3.1"
      "rc-dropdown@3.2.0"
      "rc-field-form@1.20.0"
      "rc-image@5.2.4"
      "rc-input-number@7.0.3"
      "rc-mentions@1.5.3"
      "rc-menu@8.10.6"
      "rc-motion@2.4.1"
      "rc-notification@4.5.5"
      "rc-overflow@1.0.2"
      "rc-pagination@3.1.6"
      "rc-picker@2.5.10"
      "rc-progress@3.1.3"
      "rc-rate@2.9.1"
      "rc-resize-observer@1.0.0"
      "rc-select@12.1.7"
      "rc-slider@9.7.2"
      "rc-steps@4.1.3"
      "rc-switch@3.2.2"
      "rc-table@7.13.3"
      "rc-tabs@11.7.3"
      "rc-textarea@0.3.4"
      "rc-tooltip@5.1.0"
      "rc-tree-select@4.3.1"
      "rc-tree@4.1.5"
      "rc-trigger@5.2.3"
      "rc-upload@4.2.0"
      "rc-util@5.9.8"
      "rc-virtual-list@3.2.6"
      "rc@1.2.8"
      "react-fast-compare@2.0.4"
      "react-is@16.13.1"
      "react-lifecycles-compat@3.0.4"
      "react-modal@3.12.1"
      "react-onclickoutside@6.10.0"
      "react-overlays@0.9.3"
      "react-prop-types@0.4.0"
      "react-test-renderer@16.14.0"
      "react-transition-group@2.9.0"
      "read-pkg-up@2.0.0"
      "read-pkg@2.0.0"
      "readable-stream@3.6.0"
      "readdirp@3.5.0"
      "rechoir@0.7.0"
      "recompose@0.27.1"
      "redent@3.0.0"
      "reduce-flatten@2.0.0"
      "reflect.ownkeys@0.2.0"
      "refractor@3.3.1"
      "regenerator-runtime@0.13.7"
      "regex-not@1.0.2"
      "regexp.prototype.flags@1.3.1"
      "regexpp@3.1.0"
      "remark-parse@9.0.0"
      "remark-stringify@9.0.1"
      "remark@13.0.0"
      "remove-trailing-separator@1.1.0"
      "repeat-element@1.1.3"
      "repeat-string@1.6.1"
      "repeating@2.0.1"
      "req-all@0.1.0"
      "request-promise-core@1.1.4"
      "request-promise-native@1.0.9"
      "request@2.88.2"
      "require-directory@2.1.1"
      "require-from-string@2.0.2"
      "require-main-filename@2.0.0"
      "requires-port@1.0.0"
      "resize-observer-polyfill@1.5.1"
      "resolve-cwd@3.0.0"
      "resolve-from@4.0.0"
      "resolve-pathname@3.0.0"
      "resolve-url@0.2.1"
      "resolve@1.1.7"
      "ret@0.1.15"
      "retry@0.12.0"
      "reusify@1.0.4"
      "rgb-regex@1.0.1"
      "rgba-regex@1.0.0"
      "rimraf@2.6.3"
      "ripemd160@2.0.2"
      "rst-selector-parser@2.2.3"
      "rsvp@4.8.5"
      "run-parallel-limit@1.0.6"
      "run-parallel@1.1.10"
      "run-queue@1.0.3"
      "safe-buffer@5.2.1"
      "safe-regex@1.1.0"
      "safer-buffer@2.1.2"
      "sane@4.1.0"
      "sax@1.2.4"
      "saxes@5.0.1"
      "scheduler@0.19.1"
      "schema-utils@3.0.0"
      "scroll-into-view-if-needed@2.2.28"
      "select-hose@2.0.0"
      "select@1.1.2"
      "selfsigned@1.10.8"
      "semver@7.3.4"
      "send@0.17.1"
      "serialize-javascript@5.0.1"
      "serve-index@1.9.1"
      "serve-static@1.14.1"
      "set-blocking@2.0.0"
      "set-value@2.0.1"
      "setimmediate@1.0.5"
      "setprototypeof@1.1.1"
      "sha.js@2.4.11"
      "shallow-clone@3.0.1"
      "shallowequal@1.1.0"
      "shebang-command@2.0.0"
      "shebang-regex@3.0.0"
      "shellwords@0.1.1"
      "side-channel@1.0.4"
      "sift@13.5.0"
      "signal-exit@3.0.3"
      "simple-swizzle@0.2.2"
      "sisteransi@1.0.5"
      "slash@3.0.0"
      "slice-ansi@2.1.0"
      "snapdragon-node@2.1.1"
      "snapdragon-util@3.0.1"
      "snapdragon@0.8.2"
      "snapsvg-cjs@0.0.6"
      "snapsvg@0.5.1"
      "sockjs-client@1.4.0"
      "sockjs@0.3.20"
      "source-list-map@2.0.1"
      "source-map-resolve@0.5.3"
      "source-map-support@0.5.19"
      "source-map-url@0.4.1"
      "source-map@0.6.1"
      "space-separated-tokens@1.1.5"
      "spdx-correct@3.1.1"
      "spdx-exceptions@2.3.0"
      "spdx-expression-parse@3.0.1"
      "spdx-license-ids@3.0.7"
      "spdy-transport@3.0.0"
      "spdy@4.0.2"
      "specificity@0.4.1"
      "split-string@3.1.0"
      "split2@2.2.0"
      "sprintf-js@1.0.3"
      "sshpk@1.16.1"
      "ssri@8.0.1"
      "stable@0.1.8"
      "stack-generator@2.0.5"
      "stack-utils@2.0.3"
      "stackframe@1.2.0"
      "static-extend@0.1.2"
      "statuses@1.5.0"
      "stealthy-require@1.1.1"
      "stream-each@1.2.3"
      "stream-http@2.8.3"
      "stream-shift@1.0.1"
      "string-convert@0.2.1"
      "string-length@4.0.1"
      "string-width@3.1.0"
      "string.prototype.matchall@4.0.3"
      "string.prototype.trim@1.2.3"
      "string.prototype.trimend@1.0.3"
      "string.prototype.trimstart@1.0.3"
      "string_decoder@1.3.0"
      "strip-ansi@6.0.0"
      "strip-bom@3.0.0"
      "strip-eof@1.0.0"
      "strip-final-newline@2.0.0"
      "strip-indent@3.0.0"
      "strip-json-comments@3.1.1"
      "style-search@0.1.0"
      "stylehacks@4.0.3"
      "stylelint-config-recommended@3.0.0"
      "sugarss@2.0.0"
      "supports-color@5.5.0"
      "supports-hyperlinks@2.1.0"
      "svg-tags@1.0.0"
      "svgo@1.3.2"
      "symbol-observable@1.2.0"
      "symbol-tree@3.2.4"
      "table-layout@1.0.1"
      "table@5.4.6"
      "tapable@1.1.3"
      "tar@6.1.0"
      "terminal-link@2.1.1"
      "terser@4.8.0"
      "test-exclude@6.0.0"
      "text-table@0.2.0"
      "throat@5.0.0"
      "through2@2.0.5"
      "through@2.3.8"
      "thunky@1.1.0"
      "timers-browserify@2.0.12"
      "timsort@0.3.0"
      "tiny-emitter@2.1.0"
      "tiny-invariant@1.1.0"
      "tiny-warning@1.0.3"
      "tlds@1.220.0"
      "tmpl@1.0.4"
      "to-arraybuffer@1.0.1"
      "to-fast-properties@2.0.0"
      "to-object-path@0.3.0"
      "to-regex-range@5.0.1"
      "to-regex@3.0.2"
      "toggle-selection@1.0.6"
      "toidentifier@1.0.0"
      "toposort@2.0.2"
      "tough-cookie@3.0.1"
      "tr46@2.0.2"
      "trim-newlines@3.0.0"
      "trough@1.0.5"
      "ts-essentials@2.0.12"
      "ts-invariant@0.4.4"
      "tsconfig-paths@3.9.0"
      "tslib@1.14.1"
      "tsutils@3.20.0"
      "tty-browserify@0.0.0"
      "tunnel-agent@0.6.0"
      "tween-functions@1.2.0"
      "tweetnacl@0.14.5"
      "type-check@0.3.2"
      "type-detect@4.0.8"
      "type-fest@0.8.1"
      "type-is@1.6.18"
      "typedarray-to-buffer@3.1.5"
      "typedarray@0.0.6"
      "typical@5.2.0"
      "ua-parser-js@0.7.23"
      "uc.micro@1.0.6"
      "unbox-primitive@1.0.0"
      "uncontrollable@7.2.1"
      "underscore@1.9.1"
      "unified@9.2.0"
      "union-value@1.0.1"
      "uniq@1.0.1"
      "uniqs@2.0.0"
      "unique-filename@1.1.1"
      "unique-slug@2.0.2"
      "unist-util-find-all-after@3.0.2"
      "unist-util-is@4.0.4"
      "unist-util-stringify-position@2.0.3"
      "unpipe@1.0.0"
      "unquote@1.1.1"
      "unset-value@1.0.0"
      "upath@1.2.0"
      "uri-js@4.4.1"
      "urix@0.1.0"
      "url-parse@1.4.7"
      "url@0.11.0"
      "use-composed-ref@1.1.0"
      "use-isomorphic-layout-effect@1.1.1"
      "use-latest@1.2.0"
      "use@3.1.1"
      "util-deprecate@1.0.2"
      "util.promisify@1.0.1"
      "util@0.11.1"
      "utils-merge@1.0.1"
      "uuid@3.4.0"
      "v8-compile-cache@2.2.0"
      "v8-to-istanbul@7.1.0"
      "validate-npm-package-license@3.0.4"
      "value-equal@1.0.1"
      "vary@1.1.2"
      "vendors@1.0.4"
      "verror@1.10.0"
      "vfile-message@2.0.4"
      "vfile@4.2.1"
      "vm-browserify@1.1.2"
      "void-elements@2.0.1"
      "w3c-hr-time@1.0.2"
      "w3c-xmlserializer@2.0.0"
      "walker@1.0.7"
      "warning@3.0.0"
      "watchpack-chokidar2@2.0.1"
      "watchpack@1.7.5"
      "wbuf@1.7.3"
      "webidl-conversions@6.1.0"
      "webpack-dev-middleware@3.7.3"
      "webpack-log@2.0.0"
      "webpack-merge@4.2.2"
      "webpack-sources@1.4.3"
      "websocket-driver@0.6.5"
      "websocket-extensions@0.1.4"
      "whatwg-encoding@1.0.5"
      "whatwg-fetch@3.5.0"
      "whatwg-mimetype@2.3.0"
      "whatwg-url@8.4.0"
      "which-boxed-primitive@1.0.2"
      "which-module@2.0.0"
      "which@2.0.2"
      "wildcard@2.0.0"
      "word-wrap@1.2.3"
      "wordwrapjs@4.0.0"
      "worker-farm@1.7.0"
      "wrap-ansi@6.2.0"
      "wrappy@1.0.2"
      "write-file-atomic@3.0.3"
      "write@1.0.3"
      "ws@7.4.3"
      "xml-name-validator@3.0.0"
      "xmlchars@2.2.0"
      "xtend@4.0.2"
      "y18n@4.0.1"
      "yallist@4.0.0"
      "yaml@1.10.0"
      "yargs-parser@18.1.3"
      "yargs@15.4.1"
      "yn@3.1.1"
      "yocto-queue@0.1.0"
      "zen-observable-ts@0.8.21"
      "zen-observable@0.8.15"
      "zwitch@1.0.5"
    ];
  };
}
