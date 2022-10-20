# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{self_pkg}: let
  build_check = check:
    self_pkg.overridePythonAttrs (
      old: {
        checkPhase = [old."${check}"];
      }
    );
in {
  tests = build_check "test_check";
  types = build_check "type_check";
}
