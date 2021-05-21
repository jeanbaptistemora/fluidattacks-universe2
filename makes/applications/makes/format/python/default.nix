{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "airs"
    "skims"
    "makes"
    "observes"
  ];
  name = "makes-format-python";
}
