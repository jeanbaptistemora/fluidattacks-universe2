# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  pkgs,
  lib,
  python_version,
}: let
  _python_pkgs = pkgs."${python_version}Packages";
  _python_pkgs_2 =
    _python_pkgs
    // {
      click = _python_pkgs.click.overridePythonAttrs (
        old: rec {
          version = "7.1.2";
          src = lib.fetchPypi {
            inherit version;
            pname = old.pname;
            sha256 = "0rUlXHxjSbwb0eWeCM0SrLvWPOZJ8liHVXg6qU37axo=";
          };
        }
      );
      types-requests = _python_pkgs.types-requests.overridePythonAttrs (
        old: rec {
          version = "2.27.16";
          src = lib.fetchPypi {
            inherit version;
            pname = old.pname;
            sha256 = "yAEMGLKRp++2CxRS2+ElMLwlaT3WV+cMYoA/zcS//ps=";
          };
        }
      );
    };
in
  _python_pkgs_2
  // {
    fa-purity = pkgs.fa-purity."${python_version}".pkg;
    import-linter = import ./import-linter {
      inherit lib;
      pythonPkgs = _python_pkgs_2;
    };
    pathos = import ./pathos {
      inherit lib;
      pythonPkgs = _python_pkgs_2;
    };
    postgres-client = pkgs.postgres-client."${python_version}".pkg;
    redshift-client = pkgs.redshift-client."${python_version}".pkg;
    types-click = import ./click/stubs.nix lib;
    utils-logger = pkgs.utils-logger."${python_version}".pkg;
  }
