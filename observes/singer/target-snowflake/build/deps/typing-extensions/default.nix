# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  python_pkgs,
}: let
  version = "4.3.0";
in
  python_pkgs.typing-extensions.overridePythonAttrs (
    _: {
      inherit version;
      src = lib.fetchPypi {
        inherit version;
        pname = "typing_extensions";
        sha256 = "5tJnejL0f8frJ5XbHdFcHzTv9ha8ryz7Xpl/hU+hxKY=";
      };
      postPatch = "";
    }
  )
