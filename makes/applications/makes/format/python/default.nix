{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "airs"
    "skims"
    "makes/applications/airs"
    "makes/applications/makes/okta"
    "makes/applications/skims"
    "makes/packages/airs"
    "makes/packages/skims"
    "observes"
  ];
  name = "makes-format-python";
}
