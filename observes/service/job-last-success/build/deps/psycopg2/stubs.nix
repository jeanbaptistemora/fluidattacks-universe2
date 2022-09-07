# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
lib:
lib.buildPythonPackage rec {
  pname = "types-psycopg2";
  version = "2.9.9";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "T51NUu6zQ9wA/V7U8VE6ilwY77oKBy64JwbRXPTyCi4=";
  };
}
