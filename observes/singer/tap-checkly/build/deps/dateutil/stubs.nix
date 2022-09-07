# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
lib:
lib.buildPythonPackage rec {
  pname = "types-python-dateutil";
  version = "2.8.12";
  src = lib.fetchPypi {
    inherit pname version;
    hash = "sha256:7zBTt0XwHERDtRK2s9WwT7ry1HaqUDtsyTIEah7fpWo=";
  };
}
