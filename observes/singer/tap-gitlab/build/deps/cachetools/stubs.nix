# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
lib:
lib.buildPythonPackage rec {
  pname = "types-cachetools";
  version = "5.0.1";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "K54LGs4aDeZ7w87ZxKpp//iCusi/6w8q768PmeRXHGs=";
  };
}
