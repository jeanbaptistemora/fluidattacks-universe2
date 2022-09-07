# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  src,
  metadata,
  propagatedBuildInputs,
  nativeBuildInputs,
}:
lib.buildPythonPackage rec {
  pname = metadata.name;
  version = metadata.version;
  format = "pyproject";
  arch_check = ./check/arch.sh;
  test_check = ./check/tests.sh;
  type_check = ./check/types.sh;
  installCheckPhase = [
    ''
      source ${type_check} \
      && source ${test_check} \
      && source ${arch_check}
    ''
  ];
  doCheck = true;
  pythonImportsCheck = [pname];
  inherit src propagatedBuildInputs nativeBuildInputs;
}
