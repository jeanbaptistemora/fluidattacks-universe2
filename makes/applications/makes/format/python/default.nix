{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "."
  ];
  name = "makes-format-python";
}
