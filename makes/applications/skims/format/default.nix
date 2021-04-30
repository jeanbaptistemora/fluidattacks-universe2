{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "skims"
  ];
  name = "skims-format";
}
