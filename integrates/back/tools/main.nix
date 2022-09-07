# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeSearchPaths,
  outputs,
  ...
}:
makeSearchPaths {
  source = [
    outputs."/integrates/back/tools/asciidoctor-pdf"
    outputs."/integrates/back/tools/concurrent-ruby"
    outputs."/integrates/back/tools/secure-spreadsheet"
  ];
}
