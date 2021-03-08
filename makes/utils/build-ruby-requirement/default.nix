path: pkgs:

{ dependencies ? [ ]
, name
, ruby
, requirement
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
in
makeDerivation {
  arguments = {
    envRequirement = requirement;
  };
  builder = path "/makes/utils/build-ruby-requirement/builder.sh";
  name = "build-ruby-requirement-${name}";
  searchPaths = {
    envPaths = dependencies ++ [
      pkgs.git
      pkgs.gnused
      ruby
    ];
  };
}
