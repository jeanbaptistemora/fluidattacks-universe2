{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "."
  ];
  targetsIsort = [
    "integrates"
    "skims"
  ];
  name = "makes-format-python";
}
