path: pkgs:

{ dependencies
, name
, ruby
, requirement
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
in
makeDerivation {
  builder = path "/makes/utils/build-ruby-requirement/builder.sh";
  buildInputs = dependencies ++ [
    pkgs.cacert
    pkgs.git
    ruby
  ];
  envRequirement = requirement;
  envRuby = ruby;
  envSed = "${pkgs.gnused}/bin/sed";
  name = "build-ruby-requirement-${name}";
}
