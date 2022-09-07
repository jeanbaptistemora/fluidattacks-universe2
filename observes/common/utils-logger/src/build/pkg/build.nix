# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  src,
  metadata,
  build_deps,
  runtime_deps,
  test_deps,
}:
lib.buildPythonPackage rec {
  pname = metadata.name;
  version = metadata.version;
  format = "pyproject";
  type_check = ./check/types.sh;
  checkPhase = [
    ''
      source ${type_check}
    ''
  ];
  doCheck = true;
  pythonImportsCheck = [pname];
  buildInputs = build_deps;
  propagatedBuildInputs = runtime_deps;
  checkInputs = test_deps;
  inherit src;
}
