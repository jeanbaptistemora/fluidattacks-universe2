{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "skims"
    "makes/applications/makes/okta"
    "makes/applications/skims"
    "makes/packages/skims"
    "observes"
  ];
  name = "makes-format-python";
}
