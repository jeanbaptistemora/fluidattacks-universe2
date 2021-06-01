{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "."
  ];
  targetsIsort = [
    "airs"
    "asserts"
    "integrates"
    "skims"
  ];
  name = "makes-format-python";
}
