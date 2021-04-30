{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "skims"
    "makes/applications/skims"
    "makes/packages/skims"
  ];
  name = "skims-format";
}
