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
    "docs"
    "forces"
    "makes"
    "melts"
    "integrates"
    "skims"
  ];
  name = "makes-format-python";
}
