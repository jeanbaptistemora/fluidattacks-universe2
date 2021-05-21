{ pythonFormat
, ...
}:
pythonFormat {
  targets = [
    "airs"
    "asserts"
    "build"
    "common"
    "docs"
    "forces"
    # "integrates"
    "makes"
    # "melts"
    "observes"
    "reviews"
    "skims"
    "sorts"
    "teaches"
  ];
  name = "makes-format-python";
}
