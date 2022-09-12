# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{lib}:
lib.buildPythonPackage rec {
  pname = "types-python-dateutil";
  version = "2.8.16";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "OqrEwTjra47LwlUJluwl1uRbXTKIfR5pPQhC7i+mWdI=";
  };
}
