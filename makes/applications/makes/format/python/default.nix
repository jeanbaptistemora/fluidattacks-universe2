{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "."
  ];
  targetsIsort = [
    "skims"
  ];
  name = "makes-format-python";
}
