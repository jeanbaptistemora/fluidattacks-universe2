{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "makes/applications/makes/okta"
  ];
  name = "makes-okta-format";
}
