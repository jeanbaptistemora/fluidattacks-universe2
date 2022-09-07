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
  type_check = ./check/types.sh;
  test_check = ./check/tests.sh;
  installCheckPhase = [
    ''
      source ${type_check} \
      && source ${test_check}
    ''
  ];
  doCheck = true;
  pythonImportsCheck = [pname "${pname}.exporter" "${pname}.creds"];
  inherit src propagatedBuildInputs nativeBuildInputs;
}
