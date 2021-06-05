{ bashFormat
, ...
}:
let
  fmtProduct = product: [
    product
    "makes/applications/${product}"
    "makes/packages/${product}"
  ];
in
bashFormat {
  targets = builtins.concatLists (builtins.map fmtProduct [
    "airs"
    "docs"
    "forces"
    "integrates"
    "melts"
    "observes"
    "reviews"
    "sorts"
    "skims"
  ]);
  name = "makes-format-bash";
}
