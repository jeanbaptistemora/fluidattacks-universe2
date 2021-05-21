{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "skims"
    "makes/applications/skims"
    "makes/packages/skims"
  ];
  name = "makes-format-python";
}
