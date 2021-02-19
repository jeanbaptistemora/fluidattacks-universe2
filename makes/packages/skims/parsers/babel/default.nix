{ path
, skimsPkgs
, ...
} @ _:
let
  buildNodeRequirements = import (path "/makes/utils/build-node-requirements") path skimsPkgs;
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  arguments = {
    envNodeRequirements = buildNodeRequirements {
      dependencies = [ ];
      name = "skims-parsers-babel";
      node = skimsPkgs.nodejs;
      requirements = {
        direct = [ "@babel/parser@7.11.0" ];
        inherited = [ ];
      };
    };
    envParseJs = path "/skims/static/parsers/babel/parse.js";
  };
  builder = path "/makes/packages/skims/parsers/babel/builder.sh";
  name = "skims-parsers-babel";
}
