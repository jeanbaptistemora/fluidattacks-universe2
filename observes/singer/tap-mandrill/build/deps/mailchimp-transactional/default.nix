# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  python_pkgs,
}:
lib.buildPythonPackage rec {
  pname = "mailchimp_transactional";
  format = "wheel";
  version = "1.0.47";
  src = lib.fetchPypi {
    inherit pname version format;
    dist = "py3";
    python = "py3";
    platform = "any";
    sha256 = "92i857hR4n7OQlQDxgaCEsndEfN0X9kwpIGw1AvyUag=";
  };
  nativeBuildInputs = with python_pkgs; [];
  propagatedBuildInputs = with python_pkgs; [requests six python-dateutil];
}
