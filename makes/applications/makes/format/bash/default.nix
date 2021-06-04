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
  ]);
  name = "makes-format-bash";
}
