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
    # "integrates/arch"
    # "integrates/back"
    # "integrates/charts"
    # "integrates/deploy"
    # "integrates/front"
    # "integrates/__init__.py"
    # "integrates/lambda"
    "integrates/mobile"
    "makes"
    "melts"
    "observes"
    "reviews"
    "skims"
    "sorts"
    "teaches"
  ];
  name = "makes-format-python";
}
