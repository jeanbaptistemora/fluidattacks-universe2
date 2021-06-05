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
    "skims"
  ]);
  name = "makes-format-bash";
}
