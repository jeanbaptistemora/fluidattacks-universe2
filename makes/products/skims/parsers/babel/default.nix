{ path
, skimsPkgs
, ...
} @ _:
let
  buildNodeRequirements = import (path "/makes/utils/build-node-requirements") path skimsPkgs;
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/products/skims/parsers/babel/builder.sh";
  envNodeRequirements = buildNodeRequirements {
    dependencies = [ ];
    node = skimsPkgs.nodejs;
    requirements = {
      direct = [ "@babel/parser@7.11.0" ];
      inherited = [ ];
    };
  };
  envParseJs = path "/skims/static/parsers/babel/parse.js";
  name = "skims-parsers-babel";
}
