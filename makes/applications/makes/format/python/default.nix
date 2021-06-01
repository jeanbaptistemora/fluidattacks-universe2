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
    "integrates"
    "skims"
  ];
  name = "makes-format-python";
}
