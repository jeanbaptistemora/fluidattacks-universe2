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
    "observes"
    "integrates"
    "skims"
  ];
  name = "makes-format-python";
}
