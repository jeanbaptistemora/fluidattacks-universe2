# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  libGit,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-storage-deploy";
  searchPaths = {
    bin = [
      outputs."/deployTerraform/integratesStorage"
      outputs."/testTerraform/integratesStorage"
    ];
    source = [
      libGit
      outputs."/integrates/storage/infra/lib"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
