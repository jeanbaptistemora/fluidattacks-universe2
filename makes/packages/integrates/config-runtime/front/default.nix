{ path
, integratesPkgs
, ...
} @ _:
let
  buildNodeRequirements = import (path "/makes/utils/build-node-requirements") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path integratesPkgs;
in
makeTemplate {
  arguments = {
    envNodeRequirements = buildNodeRequirements {
      dependencies = [ ];
      node = integratesPkgs.nodejs;
      requirements = {
        direct = [
          "@apollo/react-common@3.1.4"
          "@apollo/react-components@3.1.5"
          "@apollo/react-hooks@3.1.5"
          "@bugsnag/core@7.3.5"
          "@bugsnag/js@7.5.1"
          "@bugsnag/plugin-react@7.3.5"
          "@casl/ability@4.1.6"
          "@casl/react@2.1.1"
          "@rehooks/component-size@1.0.3"
          "@types/apollo-upload-client@8.1.3"
          "@types/chart.js@2.9.28"
          "@types/jquery@3.5.4"
          "@types/jsdom@16.2.5"
          "@types/lodash@4.14.165"
          "@types/mixpanel-browser@2.35.4"
          "@types/react-bootstrap@0.32.21"
          "@types/react-burger-menu@2.6.2"
          "@types/react-dom@16.9.9"
          "@types/react-fontawesome@1.6.4"
          "@types/react-native@0.63.42"
          "@types/react-notification-system@0.2.39"
          "@types/react-redux@7.1.7"
          "@types/react-router-dom@5.1.6"
          "@types/react-router@5.1.8"
          "@types/react-syntax-highlighter@13.5.0"
          "@types/react-tag-input@6.1.2"
          "@types/react-textarea-autosize@4.3.5"
          "@types/react@16.9.56"
          "@types/redux-form@8.2.3"
          "@types/revalidate@1.1.2"
          "@types/sjcl@1.0.29"
          "@types/styled-components@5.1.4"
          "@types/webpack-bugsnag-plugins@1.4.0"
          "announcekit-react@2.1.3"
          "apollo-cache-inmemory@1.6.6"
          "apollo-client@2.6.10"
          "apollo-link-error@1.1.13"
          "apollo-link-http-common@0.2.16"
          "apollo-link-ws@1.0.20"
          "apollo-link@1.2.14"
          "apollo-upload-client@13.0.0"
          "apollo-utilities@1.3.4"
          "bootstrap-switch-button-react@1.2.0"
          "bootstrap@3.4.1"
          "chart.js@2.9.4"
          "chartjs-plugin-doughnutlabel@2.0.3"
          "font-awesome@4.7.0"
          "graphql-tag@2.11.0"
          "graphql@14.7.0"
          "i18next@19.8.4"
          "jquery-comments_brainkit@1.2.8"
          "jquery@3.5.1"
          "jsdom@16.4.0"
          "lodash@4.17.20"
          "mixpanel-browser@2.39.0"
          "moment@2.29.1"
          "react-apollo-network-status@4.0.1"
          "react-bootstrap-table-next@4.0.3"
          "react-bootstrap-table2-filter@1.3.3"
          "react-bootstrap-table2-paginator@2.0.3"
          "react-bootstrap-table2-toolkit@2.1.3"
          "react-bootstrap@0.33.1"
          "react-burger-menu@2.6.17"
          "react-chartjs-2@2.11.1"
          "react-circular-progressbar@2.0.3"
          "react-datetime@3.0.4"
          "react-dnd-html5-backend@3.0.2"
          "react-dnd@11.1.3"
          "react-dom@16.14.0"
          "react-fontawesome@1.7.1"
          "react-i18next@11.7.3"
          "react-image-lightbox@5.1.1"
          "react-media@1.10.0"
          "react-notification-system@0.4.0"
          "react-phone-input-2@2.13.9"
          "react-redux@7.2.0"
          "react-router-dom@5.2.0"
          "react-router@5.2.0"
          "react-scroll-up@1.3.5"
          "react-svg@11.1.1"
          "react-syntax-highlighter@15.3.0"
          "react-tag-input@6.4.3"
          "react-textarea-autosize@8.3.0"
          "react-toastify@6.1.0"
          "react@16.14.0"
          "redux-form@8.3.2"
          "redux@4.0.5"
          "revalidate@1.2.0"
          "sjcl@1.0.8"
          "styled-components@5.2.1"
          "subscriptions-transport-ws@0.9.18"
          "tachyons@4.12.0"
        ];
        inherited = [
          "@babel/code-frame@7.12.11"
          "@babel/generator@7.12.11"
          "@babel/helper-annotate-as-pure@7.12.10"
          "@babel/helper-function-name@7.12.11"
          "@babel/helper-get-function-arity@7.12.10"
          "@babel/helper-module-imports@7.12.5"
          "@babel/helper-split-export-declaration@7.12.11"
          "@babel/helper-validator-identifier@7.12.11"
          "@babel/highlight@7.10.4"
          "@babel/parser@7.12.11"
          "@babel/runtime-corejs2@7.12.5"
          "@babel/runtime@7.12.5"
          "@babel/template@7.12.7"
          "@babel/traverse@7.12.12"
          "@babel/types@7.12.12"
          "@bugsnag/browser@7.6.0"
          "@bugsnag/cuid@3.0.0"
          "@bugsnag/node@7.6.0"
          "@bugsnag/safe-json-stringify@6.0.0"
          "@emotion/is-prop-valid@0.8.8"
          "@emotion/memoize@0.7.4"
          "@emotion/stylis@0.8.5"
          "@emotion/unitless@0.7.5"
          "@react-dnd/asap@4.0.0"
          "@react-dnd/invariant@2.0.0"
          "@react-dnd/shallowequal@2.0.0"
          "@tanem/svg-injector@8.2.2"
          "@types/anymatch@1.3.1"
          "@types/extract-files@8.1.0"
          "@types/hast@2.3.1"
          "@types/history@4.7.8"
          "@types/hoist-non-react-statics@3.3.1"
          "@types/invariant@2.2.34"
          "@types/node@14.14.22"
          "@types/parse5@6.0.0"
          "@types/prop-types@15.7.3"
          "@types/redux@3.6.0"
          "@types/sizzle@2.3.2"
          "@types/source-list-map@0.1.2"
          "@types/tapable@1.0.6"
          "@types/tough-cookie@4.0.0"
          "@types/uglify-js@3.11.1"
          "@types/unist@2.0.3"
          "@types/webpack-sources@2.1.0"
          "@types/webpack@4.41.26"
          "@types/zen-observable@0.8.2"
          "@wry/context@0.4.4"
          "@wry/equality@0.1.11"
          "abab@2.0.5"
          "acorn-globals@6.0.0"
          "acorn-walk@7.2.0"
          "acorn@7.4.1"
          "ajv@6.12.6"
          "amdefine@1.0.1"
          "ansi-styles@3.2.1"
          "apollo-cache@1.3.5"
          "asap@2.0.6"
          "asn1@0.2.4"
          "assert-plus@1.0.0"
          "ast-transform@0.0.0"
          "ast-types@0.7.8"
          "async-limiter@1.0.1"
          "asynckit@0.4.0"
          "autobind-decorator@2.4.0"
          "aws-sign2@0.7.0"
          "aws4@1.11.0"
          "babel-plugin-styled-components@1.12.0"
          "babel-plugin-syntax-jsx@6.18.0"
          "backo2@1.0.2"
          "bcrypt-pbkdf@1.0.2"
          "browser-process-hrtime@1.0.0"
          "browser-resolve@1.11.3"
          "browserify-optional@1.0.1"
          "byline@5.0.0"
          "camelize@1.0.0"
          "caseless@0.12.0"
          "chalk@2.4.2"
          "character-entities-legacy@1.1.4"
          "character-entities@1.2.4"
          "character-reference-invalid@1.1.4"
          "chartjs-color-string@0.6.0"
          "chartjs-color@2.4.1"
          "classnames@2.2.6"
          "clipboard@2.0.6"
          "clsx@1.1.1"
          "color-convert@1.9.3"
          "color-name@1.1.4"
          "combined-stream@1.0.8"
          "comma-separated-tokens@1.0.8"
          "content-type@1.0.4"
          "core-js@2.6.12"
          "core-util-is@1.0.2"
          "css-color-keywords@1.0.0"
          "css-to-react-native@3.0.0"
          "cssom@0.4.4"
          "cssstyle@2.3.0"
          "csstype@3.0.6"
          "dashdash@1.14.1"
          "data-urls@2.0.0"
          "debug@4.3.1"
          "decimal.js@10.2.1"
          "deep-is@0.1.3"
          "delayed-stream@1.0.0"
          "delegate@3.2.0"
          "detect-passive-events@1.0.5"
          "dnd-core@11.1.3"
          "dom-helpers@3.4.0"
          "domexception@2.0.1"
          "ecc-jsbn@0.1.2"
          "end-of-stream@1.4.4"
          "error-stack-parser@2.0.6"
          "es6-error@4.1.1"
          "escape-string-regexp@1.0.5"
          "escodegen@1.14.3"
          "esprima@4.0.1"
          "estraverse@4.3.0"
          "esutils@2.0.3"
          "eve@0.5.4"
          "eventemitter3@3.1.2"
          "exenv@1.2.2"
          "extend@3.0.2"
          "extract-files@8.1.0"
          "extsprintf@1.3.0"
          "fast-deep-equal@3.1.3"
          "fast-json-stable-stringify@2.1.0"
          "fast-levenshtein@2.0.6"
          "fault@1.0.4"
          "file-saver@2.0.2"
          "forever-agent@0.6.1"
          "form-data@2.3.3"
          "format@0.2.2"
          "getpass@0.1.7"
          "globals@11.12.0"
          "good-listener@1.2.2"
          "har-schema@2.0.0"
          "har-validator@5.1.5"
          "has-flag@3.0.0"
          "hast-util-parse-selector@2.2.5"
          "hastscript@6.0.0"
          "highlight.js@10.5.0"
          "history@4.10.1"
          "hoist-non-react-statics@3.3.2"
          "html-encoding-sniffer@2.0.1"
          "html-parse-stringify2@2.0.1"
          "http-signature@1.2.0"
          "iconv-lite@0.4.24"
          "invariant@2.2.4"
          "ip-regex@2.1.0"
          "is-alphabetical@1.0.4"
          "is-alphanumerical@1.0.4"
          "is-decimal@1.0.4"
          "is-hexadecimal@1.0.4"
          "is-potential-custom-element-name@1.0.0"
          "is-promise@2.2.2"
          "is-typedarray@1.0.0"
          "isarray@0.0.1"
          "iserror@0.0.2"
          "isstream@0.1.2"
          "iterall@1.3.0"
          "js-tokens@4.0.0"
          "jsbn@0.1.1"
          "jsesc@2.5.2"
          "json-schema-traverse@0.4.1"
          "json-schema@0.2.3"
          "json-stringify-safe@5.0.1"
          "json2mq@0.2.0"
          "jsprim@1.4.1"
          "keycode@2.2.0"
          "levn@0.3.0"
          "lodash-es@4.17.20"
          "lodash.debounce@4.0.8"
          "lodash.memoize@4.1.2"
          "lodash.reduce@4.6.0"
          "lodash.sortby@4.7.0"
          "lodash.startswith@4.2.1"
          "loose-envify@1.4.0"
          "lowlight@1.18.0"
          "mime-db@1.45.0"
          "mime-types@2.1.28"
          "mini-create-react-context@0.4.1"
          "ms@2.1.2"
          "nwsapi@2.2.0"
          "oauth-sign@0.9.0"
          "object-assign@4.1.1"
          "once@1.4.0"
          "optimism@0.10.3"
          "optionator@0.8.3"
          "parse-entities@2.0.0"
          "parse5@5.1.1"
          "path-to-regexp@1.8.0"
          "performance-now@2.1.0"
          "postcss-value-parser@4.1.0"
          "prelude-ls@1.1.2"
          "prismjs@1.23.0"
          "prop-types-extra@1.1.1"
          "prop-types@15.7.2"
          "property-information@5.6.0"
          "psl@1.8.0"
          "pump@3.0.0"
          "punycode@2.1.1"
          "qs@6.5.2"
          "react-fast-compare@2.0.4"
          "react-is@16.13.1"
          "react-lifecycles-compat@3.0.4"
          "react-modal@3.12.1"
          "react-overlays@0.9.3"
          "react-prop-types@0.4.0"
          "react-transition-group@2.9.0"
          "refractor@3.3.1"
          "regenerator-runtime@0.13.7"
          "request-promise-core@1.1.4"
          "request-promise-native@1.0.9"
          "request@2.88.2"
          "resolve-pathname@3.0.0"
          "resolve@1.1.7"
          "safe-buffer@5.2.1"
          "safer-buffer@2.1.2"
          "saxes@5.0.1"
          "scheduler@0.19.1"
          "select@1.1.2"
          "shallowequal@1.1.0"
          "sift@13.5.0"
          "snapsvg-cjs@0.0.6"
          "snapsvg@0.5.1"
          "source-map@0.6.1"
          "space-separated-tokens@1.1.5"
          "sshpk@1.16.1"
          "stack-generator@2.0.5"
          "stackframe@1.2.0"
          "stealthy-require@1.1.1"
          "string-convert@0.2.1"
          "supports-color@5.5.0"
          "symbol-observable@1.2.0"
          "symbol-tree@3.2.4"
          "through@2.3.8"
          "tiny-emitter@2.1.0"
          "tiny-invariant@1.1.0"
          "tiny-warning@1.0.3"
          "to-fast-properties@2.0.0"
          "tough-cookie@3.0.1"
          "tr46@2.0.2"
          "ts-essentials@2.0.12"
          "ts-invariant@0.4.4"
          "tslib@1.14.1"
          "tunnel-agent@0.6.0"
          "tween-functions@1.2.0"
          "tweetnacl@0.14.5"
          "type-check@0.3.2"
          "uncontrollable@7.1.1"
          "underscore@1.9.1"
          "uri-js@4.4.1"
          "use-composed-ref@1.1.0"
          "use-isomorphic-layout-effect@1.1.1"
          "use-latest@1.2.0"
          "uuid@3.4.0"
          "value-equal@1.0.1"
          "verror@1.10.0"
          "void-elements@2.0.1"
          "w3c-hr-time@1.0.2"
          "w3c-xmlserializer@2.0.0"
          "warning@3.0.0"
          "webidl-conversions@6.1.0"
          "whatwg-encoding@1.0.5"
          "whatwg-mimetype@2.3.0"
          "whatwg-url@8.4.0"
          "word-wrap@1.2.3"
          "wrappy@1.0.2"
          "ws@7.4.2"
          "xml-name-validator@3.0.0"
          "xmlchars@2.2.0"
          "xtend@4.0.2"
          "zen-observable-ts@0.8.21"
          "zen-observable@0.8.15"
        ];
      };
    };
    envSearchPaths = makeSearchPaths [ ];
  };
  name = "integrates-config-runtime-front";
  template = path "/makes/packages/integrates/config-runtime/front/template.sh";
}
