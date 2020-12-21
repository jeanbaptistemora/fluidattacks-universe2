attrs @ {
  pkgsSkims,
  self,
  ...
}:

let
  make = import ../../../makes/utils/make pkgsSkims;
in
  make {
    builder = ./builder.sh;
    buildInputs = [
    ];
    envANTLR = import ../../../makes/skims/parsers/antlr {
      inherit pkgsSkims;
    };
    envSrcEntry = ../../../makes/skims/bin/entry.sh;
    envSrcSkimsSkims = ../../../skims/skims;
    envSrcSkimsStatic = ../../../skims/static;
    envSrcSkimsVendor = ../../../skims/vendor;
    name = "skims-bin";
  }
