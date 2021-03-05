{ path
, nixpkgs
, ...
}:
let
  buildNodeRequirements = import (path "/makes/utils/build-node-requirements") path nixpkgs;
  makeDerivation = import (path "/makes/utils/make-derivation") path nixpkgs;
in
makeDerivation {
  arguments = {
    envNodeRequirements = buildNodeRequirements {
      dependencies = [ ];
      name = "skims-parsers-babel";
      node = nixpkgs.nodejs;
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
